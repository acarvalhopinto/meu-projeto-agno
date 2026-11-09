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
    instructions="Use tabelas para mostrar a informação final. Não incluia nenhum outro texto",
    add_history_to_context=True,
    db=db,
    num_history_runs=3
)

agent.print_response("Qual a cotação da Vale hoje ?", stream=True, session_id="petrobras_session", user_id="analista_petrobras")
agent.print_response("Qual a cotação da Petrobras hoje ?", stream=True , session_id="vale_session", user_id="analista_vale")
agent.print_response("Quais as cotações feitas hoje ?", stream=True , session_id="petrobras_session", user_id="analista_empresa")