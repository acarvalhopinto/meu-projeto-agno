from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.vectordb.chroma import ChromaDb

from agno.models.groq import Groq

from fastapi import FastAPI
import uvicorn
import asyncio

import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

vector_db = ChromaDb(collection="pdf_agent", path="tmp/chromadb", persistent_client=True)
knowledge = Knowledge(vector_db=vector_db)

knowledge.insert(
    path="D:\Asimov\Criando Agentes de IA com Agno\Projeto\Curso Agno\2588_PR_2T26.pdf", 
    metadata={"source":"Grendene", "type": "pdf", "description": "Relatório Trimestral"}, 
    skip_if_exists=True,
    reader=PDFReader()
)

db = SqliteDb(session_table="agent_session", db_file="tmp/agent.db")

agent = Agent(
    name="Agente de PDF",
    model= Groq(id="openai/gpt-oss-120b"),
    db=db,
    knowledge=knowledge,
    instructions="Você deve chamar o usuário de senhor",
    description="",
    search_knowledge=True, 
    num_history_runs=3,
    debug_mode=True
)


agent.print_response("Qual foi o Receita liquida do 2T26 vs. 2T25") ;