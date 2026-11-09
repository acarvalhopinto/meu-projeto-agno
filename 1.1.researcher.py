import os
from agno.agent import Agent
from agno.tools.tavily import TavilyTools
from agno.models.groq import Groq
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

agent = Agent(
    model= Groq(id="openai/gpt-oss-120b"),
    tools=[TavilyTools()]
)

agent.print_response("Use suas ferramentas para pesquisar a temperatura hoje em Mauá/SP")