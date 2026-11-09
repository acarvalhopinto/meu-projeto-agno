import os
from agno.agent import Agent
from agno.tools.tavily import TavilyTools
from agno.models.groq import Groq
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def celsius_to_fh(temp: float):
    """
    Converte uma temperatura em graus Celsius para Fahrenheit.
    Args:
        temp ( float): Temperatura para graus Celsius
    
    Return:
        float: Temperatura convertida
    """
    return (temp * 9/5) + 32 

agent = Agent(
    model= Groq(id="openai/gpt-oss-120b"),
    tools=[TavilyTools(), 
           celsius_to_fh,]
)

agent.print_response("Use suas ferramentas para pesquisar a temperatura hoje em Mauá/SP EM Fahrenheit")