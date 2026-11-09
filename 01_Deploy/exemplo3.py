# Imports

import requests
import json
from pprint import pprint

AGENT_ID = "agente_pdf"
ENDPOINT = f"http://localhost:7777/agents/{AGENT_ID}/runs"


# Conect Agno
def get_response_stream(message: str):
    response = requests.post(url=ENDPOINT, 
                             data = {"message":message, 
                                     "stream":"true"},
                                     stream=True)
    


    #2 - Streaming
    for line in response.iter_lines():
        if line:
            if line.startswith(b'data: '):
                data = line[6:]
                try:
                    event = json.loads(data)
                    yield event
                except json.JSONDecodeError:
                        continue

# 3 - Print resposta
def print_streaming_response(message: str):
     for event in get_response_stream(message):
        event_type = event.get("event","")
        
        # Início da execução
        if event_type == "RunStarted":
            print("Execução iniciada...")
            print("-"*50)

        # Conteúdo da resposta
        elif event_type == "RunContent":
            content = event.get("content", "")
            if content:
                print(content, end="", flush=True)
            
        # Tool call iniciado
        elif event_type == "ToolCallStarted":
            tool = event.get("tool", {})
            tool_name = tool.get("tool_name", "Unknown")
            tool_args = tool.get("tool_args", {})
            print(f"TOOL INICIADA: {tool_name}")
            print(f"ARGUMENTOS: {json.dumps(tool_args, indent=2)}")

        elif event_type == "ToolCallCompleted":
            tool_name = event.get("tool", {}).get("tool_name")
            print(f"TOOL CONCLUÍDA: {tool_name}")
            print("-"*50)
        
        elif event_type == "RunCompleted":
            print("Execução concluída!")
            metrics = event.get("metrics", {})
            if metrics:
                print(f"MÉTRICAS: {json.dumps(metrics, indent=2)}")
            print("-"*50)

#4 Run ( Loop )
if __name__ == "__main__":
    message = input("Digite a Mensagem: ")
    print_streaming_response( message)
    while True:
        message = input("Digite a Mensagem: ")
        print_streaming_response( message)
  