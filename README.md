# AI SDK Python Streaming Preview


To run the example locally you need to:

1. Sign up for accounts with the AI providers you want to use (e.g., OpenAI, Anthropic).
2. Obtain API keys for each provider.
3. Set the required environment variables in `.env.local` file
    - OPENAI_API_KEY = "sk..."
    - PYTHON_LOCATION = "local"
4. `pnpm install` to install the required Node dependencies.
5. `virtualenv venv` to create a virtual environment.
6. `source venv/bin/activate` to activate the virtual environment.
7. `pip install -r requirements.txt` to install the required Python dependencies.
8. if you want to modify both the python and the frontend, run `pnpm dev` to launch the development server.
   if you want to modify only the python, run `pnpm fastapi-dev` to launch the development server. To display the frontend, run `pnpm build` and then `pnpm start` in a new terminal.

## Learn More

To learn more about the AI SDK or Next.js by Vercel, take a look at the following resources:

- [AI SDK Documentation](https://sdk.vercel.ai/docs)
- [Next.js Documentation](https://nextjs.org/docs)
