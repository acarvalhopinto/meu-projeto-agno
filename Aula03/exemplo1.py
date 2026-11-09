from fastapi   import FastAPI 
import uvicorn

app = FastAPI(title="FastAPI Andre Carvalho",
              description="API de teste", 
              version="1.0.0", 
              contact={"name": "André Carvalho", "email":"andrecarvalhopinto@gmail.com"}, )

@app.get("/")
def read_root():
    return {"message":"Heloooooo"}

@app.get("/hello/{name}")
def read_hello_name(name: str):
    return {"message": f"Heloooooo {name}"}



if __name__ == "__main__":
    uvicorn.run("exemplo1:app", host="127.0.0.1", port=8000, reload=True)