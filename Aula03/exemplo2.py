# Conta Corrente Bancaria FastAPI
# Gerenciar movimentações
# Saldo e evolução de movimentação

from fastapi   import FastAPI 
import uvicorn
from pydantic import BaseModel, Field


app = FastAPI(title="Conta Bancaria - Conta Corrente",
              description="API de teste", 
              version="1.0.0", 
              contact={"name": "André Carvalho", "email":"andrecarvalhopinto@gmail.com"}, )


# clientes
db_clientes = {"Joao": 0, 
               "Maria": 0,
               "Pedro": 0}


# Classe para movimentações
class Movimentacao(BaseModel):
    cliente: str = Field(..., description="Nome do cliente")
    valor: float = Field(..., gt=0,  description="Valor da movimentação")


@app.get("/")
def read_root():
    return {"message":"Conta Bancaria - Conta Corrente"}


# endpoint saldo
@app.post("/saldo")
def saldo(cliente: str):
    return {"message":f"Saldo do cliente {cliente} é {db_clientes[cliente]}"}

# endpoint saques
@app.post("/saque")
def saque(movimetacao: Movimentacao):
    db_clientes[movimetacao.cliente] -= movimetacao.valor
    return {"message":{ "Cliente":movimetacao.cliente, "Movimentação": -movimetacao.valor,  "Saldo":  db_clientes[movimetacao.cliente]}}
    


# endpoint deposito\
@app.post("/deposito")
def deposito(movimetacao: Movimentacao):
    db_clientes[movimetacao.cliente] += movimetacao.valor
    return {"message":{ "Cliente":movimetacao.cliente, "Movimentação"movimetacao.valor,  "Saldo":  db_clientes[movimetacao.cliente]}}




if __name__ == "__main__":
    uvicorn.run("exemplo2:app", host="127.0.0.1", port=8000, reload=True)