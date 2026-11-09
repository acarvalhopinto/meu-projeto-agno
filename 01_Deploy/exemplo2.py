import os
from pathlib import Path

from dotenv import load_dotenv, find_dotenv

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.chunking.fixed import FixedSizeChunking
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.knowledge.embedder.sentence_transformer import SentenceTransformerEmbedder
from agno.models.groq import Groq
from agno.vectordb.chroma import ChromaDb
from agno.os import AgentOS

load_dotenv(find_dotenv())

assert os.getenv("GROQ_API_KEY"), "Defina GROQ_API_KEY no arquivo .env"

PDF_PATH = Path(r"D:\Asimov\Criando Agentes de IA com Agno\Projeto\Curso Agno\2588_PR_2T26.pdf")
assert PDF_PATH.exists(), f"PDF não encontrado: {PDF_PATH}"

embedder = SentenceTransformerEmbedder(
    id="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    dimensions=384,
)

# Coleção NOVA (v3): os chunks agora são menores, então precisa reindexar.
vector_db = ChromaDb(
    collection="pdf_agent_v3",
    path="tmp/chromadb",
    persistent_client=True,
    embedder=embedder,
)

# max_results=3 -> só 3 trechos vão para o prompt (o padrão é bem maior e estoura o limite do Groq)
knowledge = Knowledge(vector_db=vector_db, max_results=3)

# Chunks pequenos (~1000 caracteres) para não inflar o prompt
reader = PDFReader(
    chunking_strategy=FixedSizeChunking(chunk_size=1000, overlap=100),
)

knowledge.insert(
    path=str(PDF_PATH),
    metadata={"source": "Grendene", "type": "pdf", "description": "Relatório Trimestral 2T26"},
    skip_if_exists=True,
    reader=reader,
)

db = SqliteDb(session_table="agent_session", db_file="tmp/agent.db")

agent = Agent(
    id="agente_pdf",
    name="Agente de PDF",
    model=Groq(
        id="openai/gpt-oss-120b",
        max_tokens=1500,                              # limita a resposta (conta para o TPM)
        request_params={"reasoning_effort": "low"},   # menos tokens gastos com raciocínio
    ),
    db=db,
    knowledge=knowledge,
    search_knowledge=True,
    add_history_to_context=True,
    num_history_runs=1,               # menos histórico = menos tokens
    enable_agentic_memory=True, 
    instructions=[
        "Chame o usuário de senhor.",
        "Sempre busque na base de conhecimento antes de responder.",
        "Responda apenas com base nos documentos; se não encontrar, diga que não encontrou.",
        "Seja objetivo e responda em português do Brasil.",
    ],
    markdown=True,
    debug_mode=False,  # debug_mode=True imprime muito; ligue só se precisar
)

# AGENT OS  ===========================================================
agent_os = AgentOS(
    name="Agente de PDF",
    agents=[agent],
    # Origens do Agent UI liberadas no CORS (localhost, 127.0.0.1 e IP da rede)
    cors_allowed_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://192.168.15.187:3000",
    ],
)
app = agent_os.get_app()

@app.post("/agente_pdf")
def agente_pdf(pergunta: str):
    response = agent.run(pergunta)
    message = response.messages[-1]
    return {"message": message.content}

if __name__ == "__main__":
    knowledge.insert(
        path=str(PDF_PATH),
        metadata={"source": "Grendene", "type": "pdf", "description": "Relatório Trimestral 2T26"},
        skip_if_exists=True,
        reader=reader,
        )
    agent_os.serve(app="exemplo2:app", reload=True)