import os
import json
from typing import List
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
from .utils.prompt import ClientMessage, convert_to_openai_messages
from .utils.tools import get_current_weather
from langchain_openai import ChatOpenAI
from langchain.schema.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage

load_dotenv(".env.local")

app = FastAPI()


class Request(BaseModel):
    messages: List[ClientMessage]


available_tools = {
    "get_current_weather": get_current_weather,
}

def convert_openai_messages_to_langchain(messages: List[ChatCompletionMessageParam]):
    # Convert OpenAI messages to LangChain messages
    langchain_messages = []
    for msg in messages:
        if msg["role"] == "user":
            content = msg["content"][0]["text"] if isinstance(msg["content"], list) else msg["content"]
            langchain_messages.append(HumanMessage(content=content))
        elif msg["role"] == "assistant":
            # Handle assistant messages with tool calls
            if "tool_calls" in msg and msg["tool_calls"] is not None:
                content = msg.get("content", "")
                langchain_messages.append(AIMessage(
                    content=content,
                    additional_kwargs={"tool_calls": msg["tool_calls"]}
                ))
            else:
                content = msg["content"][0]["text"] if isinstance(msg["content"], list) else msg["content"]
                langchain_messages.append(AIMessage(content=content))
        elif msg["role"] == "tool":
            # Only add tool messages if they are responses to tool calls
            langchain_messages.append(ToolMessage(
                content=msg["content"],
                tool_call_id=msg["tool_call_id"],
                name=msg.get("name", "")  # Add tool name if available
            ))
        elif msg["role"] == "system":
            langchain_messages.append(SystemMessage(content=msg["content"]))
            
    return langchain_messages

async def stream_text(messages: List[ChatCompletionMessageParam], protocol: str = 'data'):
    draft_tool_calls = []

    llm = ChatOpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        model="gpt-4o",
        streaming=True,
        stream_usage=True
    )
    
    langchain_messages = convert_openai_messages_to_langchain(messages=messages)

    async for chunk in llm.astream(input=langchain_messages):
        if hasattr(chunk, 'content') and chunk.content:
            yield '0:{text}\n'.format(text=json.dumps(chunk.content))
        elif hasattr(chunk, 'additional_kwargs') and chunk.additional_kwargs.get('tool_calls'):
            if len(draft_tool_calls) == 0:
                draft_tool_calls.append({
                    "id": chunk.tool_call_chunks[0].get('id'),
                    "name": chunk.tool_call_chunks[0].get('name'),
                    "arguments": chunk.tool_call_chunks[0].get('args')
                })
            else:
                draft_tool_calls[0]["arguments"] += chunk.tool_call_chunks[0].get('args')
        elif hasattr(chunk, 'response_metadata') and chunk.response_metadata.get('finish_reason'):
            if chunk.response_metadata.get('finish_reason') == "tool_calls":
                for tool_call in draft_tool_calls:
                    yield '9:{{"toolCallId":"{id}","toolName":"{name}","args":{args}}}\n'.format(
                        id=tool_call['id'],
                        name=tool_call['name'],
                        args=tool_call['arguments'])
                    tool_result = available_tools[tool_call['name']].invoke(input=json.loads(tool_call['arguments']))

                    yield 'a:{{"toolCallId":"{id}","toolName":"{name}","args":{args},"result":{result}}}\n'.format(
                        id=tool_call['id'],
                        name=tool_call['name'],
                        args=tool_call['arguments'],
                        result=json.dumps(tool_result))
            else:
                yield '0:{text}\n'.format(text=json.dumps(chunk.content))
        elif hasattr(chunk, 'usage_metadata') and chunk.usage_metadata:
            usage = chunk.usage_metadata
            prompt_tokens = usage.get('input_tokens')
            completion_tokens = usage.get('output_tokens')

            yield 'e:{{"finishReason":"{reason}","usage":{{"promptTokens":{prompt},"completionTokens":{completion}}},"isContinued":false}}\n'.format(
                reason="tool-calls" if len(
                    draft_tool_calls) > 0 else "stop",
                prompt=prompt_tokens,
                completion=completion_tokens
            )




@app.post("/api/chat")
async def handle_chat_data(request: Request, protocol: str = Query('data')):
    messages = request.messages
    openai_messages = convert_to_openai_messages(messages)

    response = StreamingResponse(stream_text(openai_messages, protocol))
    response.headers['x-vercel-ai-data-stream'] = 'v1'
    return response
