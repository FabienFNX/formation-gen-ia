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


# Exercices

## Jour 1

- Premier exercice : 
   - Lorsque vous allez demander au chatbot un thème, par exemple "git", celui-ci doit vous répondre par une question sur ce thème avec différentes possibilités de réponses.
   - Lorsque vous allez répondre à la question, le chatbot doit vous répondre avec la bonne réponse.

- Deuxième exercice :
    - Mettre en place un jeu de rôle avec le chatbot pour tester le candidat sur sa capacité à répondre à des questions sur un thème donné.


## Jour 2

- Réutiliser le code de la journée 1 pour créer des questions ouvertes afin de tester le candidat sur sa capacité à répondre à des questions sur un thème donné. Le logiciel devra être en mesure de noter la réponse du candidat sur une échelle de 0 à 10 et justifier sa note.


## Jour 3

- Utiliser le code intégrant Langchain pour créer un chatbot capable de répondre à des questions sur un thème donné.
- Utiliser le code intégrant Langchain pour créer un chatbot capable de répondre à des questions sur git en utilisant une chaine de RAG avec le fichier présent dans le dossier "assets".
