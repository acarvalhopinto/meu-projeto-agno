from agno.models.groq import Groq
from agno.models.message import Message

from dotenv import load_dotenv
load_dotenv()

model = Groq(id="openai/gpt-oss-120b")

message = Message(
    role="user",
    content="Ola, eu me chamo André"
)

response = model.response([message])

print(response.content)

message = Message(
    role="user",
    content="Como seria o meu nome André em Aramico ?"
)

response = model.response([message])

print(response.content)