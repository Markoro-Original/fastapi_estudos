from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/hello_world")
def hello_world():
    return{"mensagem": "Hello World!"}

@app.get("/teste")
def mudanca():
    return{"mensagem": "Mudança com server live!"}

@app.get("/soma/{num1}/{num2}") #qualquer método funciona, mas por convensão, o correto seria usar post
def soma(num1: int, num2: int):
    total = num1 + num2
    return {"resultado": total}

@app.post("/soma_body")
def soma_body(num1: int, num2: int):
    total = num1 + num2
    return {"resultado": total}

class Numero(BaseModel):
    numero1: int
    numero2: int

@app.post("/soma_pydantic")
def soma_pydantic(num: Numero):
    total = num.numero1 + num.numero2
    return {"resultado": total}

class Resultado(BaseModel):
    resultado: int

@app.post("/soma_com_response_model", response_model=Resultado)
def soma_response_model(num: Numero):
    total = num.numero1 + num.numero2
    return {"resultado": total}

@app.post("/soma_com_response_model_2")
def soma_response_model_2(num: Numero) -> Resultado:
    total = num.numero1 + num.numero2
    return {"resultado": total}