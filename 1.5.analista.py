import os
from agno.agent import Agent
from agno.tools.tavily import TavilyTools
from agno.tools.yfinance import YFinanceTools

from agno.db.sqlite import SqliteDb

from agno.models.groq import Groq
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

db = SqliteDb(db_file="tmp/data.db")

agent = Agent(
    name="analista_financeiro",
    model= Groq(id="openai/gpt-oss-120b"),
    #model= Groq(id="llama-3.3-70b-versatile"),
    tools=[YFinanceTools()],
    instructions="Voce é uma analista e tem diferentes clientes, Lemvre-se de cada cliente, suas informações e preferencias. ",
    add_history_to_context=True,
    db=db,
    num_history_runs=3, 
    enable_agentic_memory=True, 
    add_memories_to_context=True,
)

#agent.print_response("Ola, prefiro as respostas em formato de tabelas, gosto de poucas informacoes.", session_id="petrobras_session_1", user_id="analista_petrobras")
#agent.print_response("Ola, prefiro as respostas em formato de texto, gosto de bastante detalhes.", session_id="vale_session_1", user_id="analista_vale")

agent.print_response("Qual é a cotação da petrobras?", session_id="petrobras_session_2", user_id="analista_petrobras")
agent.print_response("Qual é a cotação da vale?", session_id="vale_session_2", user_id="analista_vale")
