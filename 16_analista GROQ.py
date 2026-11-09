import os
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# 1. Configurar as chaves de API
os.environ["GROQ_API_KEY"] = "SUA_API_KEY_AQUI"

# 2. Definir a Base de Conhecimento (Seus dados)
# Em um cenário real, você pode carregar PDFs usando o PyPDFLoader do LangChain
documentos_da_empresa = [
    "A política de reembolso da nossa empresa permite devoluções em até 30 dias após a compra.",
    "O suporte técnico funciona de segunda a sexta, das 9h às 18h, via chat e e-mail.",
    "O plano de saúde corporativo cobre consultas gerais, exames básicos e atendimento odontológico."
]

# 3. Criar a camada de Embeddings (Representação matemática do texto)
# Usaremos um modelo leve e gratuito da Hugging Face que roda localmente
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 4. Criar o Banco de Dados Vetorial (ChromaDB)
# Ele armazena os textos indexados pelos embeddings para busca rápida
vector_store = Chroma.from_texts(texts=documentos_da_empresa, embedding=embeddings)
retriever = vector_store.as_retriever(search_kwargs={"k": 2}) # Retorna os 2 trechos mais relevantes

# 5. Configurar o LLM no Groq
# Usando o Llama 3 para máxima velocidade e contexto
llm = ChatGroq(model="llama3-8b-8192", temperature=0.2)

# 6. Criar o Prompt do Sistema (Instruções para o modelo)
system_prompt = (
    "Você é um assistente virtual prestativo. Use os seguintes pedaços de contexto recuperados "
    "para responder à pergunta de forma direta. Se você não souber a resposta ou ela não estiver "
    "no contexto, diga apenas que não encontrou a informação.\n\n"
    "Contexto:\n{context}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

# 7. Unir tudo em uma Cadeia de RAG
question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

# 8. Testar o Sistema de RAG
pergunta = "Posso devolver um produto comprado há duas semanas e qual o horário do suporte?"
resposta = rag_chain.invoke({"input": pergunta})

print(f"Pergunta: {pergunta}\n")
print(f"Resposta do Groq RAG:\n{resposta['answer']}")
