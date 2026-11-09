# from agno.models.openai import OpenAIChat
from agno.models.groq import Groq
from agno.models.message import Message

from dotenv import load_dotenv
load_dotenv()


model = Groq(id="openai/gpt-oss-120b")

msg = Message(
    role="user",
    content=[{"type": "text", "text": "Olá, meu nome é André"}]
)

response = model.invoke([msg])

response.choices[0].message.content