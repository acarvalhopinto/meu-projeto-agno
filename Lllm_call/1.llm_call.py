import os
from groq import Groq

# O cliente busca automaticamente a variável de ambiente GROQ_API_KEY
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Faz a chamada para a API utilizando o modelo Llama
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "Você é um assistente prestativo e responde de forma concisa em português."
        },
        {
            "role": "user",
            "content": "Explique brevemente por que o Groq é tão rápido.",
        }
    ],
    # Você pode alterar para outros modelos disponíveis, como o llama-3.1-8b-instant
    model="openai/gpt-oss-120b",
    temperature=0.7,
)

# Exibe a resposta gerada pelo modelo no terminal
print(chat_completion.choices[0].message.content)
