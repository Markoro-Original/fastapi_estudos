from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel
from enum import Enum

API_KEY = "auth"
DEV_KEY = "coffee"

class Auth(BaseModel):
    api_key: str = ""
    dev_key: str = ""

def verificacao_api_key(key: Auth):
    if key.api_key != API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="API key não altorizada!")
    
    return {"api_key": key.api_key}


description = f"""
    API desenvolvida para fins de estudo do FastAPI

    - /hello_world*: retorna uma mensagem pra boa sorte.
    - /soma/num1/num2: recebe dois números pelo header e retorna a soma
    - /soma_body: recebe dois números pelo corpo da requisição e retorna a soma
    - /soma_pydantic: recebe dois números, usando um BaseModel da biblioteca pydantic
    - /soma_com_response_model: implementação de schema da resposta da requisição
"""

app = FastAPI(
    title="API para estudos",
    description=description,
    version="0.2",
    contact={
        "name": "Marcos",
        "url": "https://github.com/Markoro-Original",
    },
    dependencies=[Depends(verificacao_api_key)]    
)

class NomeGrupo(str, Enum):
    texto = "String"
    hello_world = "Hello world"
    operacao = "Operação matemática"
    teste = "Teste"

@app.get("/v1/hello_world", tags=[NomeGrupo.hello_world, NomeGrupo.texto], status_code=status.HTTP_201_CREATED)
def hello_world():
    return{"mensagem": "Hello World!"}



@app.get("/v1/teste",
         summary="Retorna uma mensagem de teste",
         description="Endpoint usado apenas para testar a edição do código com server live.",
         tags=[NomeGrupo.teste, NomeGrupo.texto],
         status_code=status.HTTP_202_ACCEPTED)
def mudanca():
    return{"mensagem": "Mudança com server live!"}



@app.get("/v1/soma/{num1}/{num2}", tags=[NomeGrupo.operacao], status_code=status.HTTP_200_OK) #qualquer método funciona, mas por convenção, o correto seria usar post
def soma(num1: int, num2: int):
    total = num1 + num2
    
    if total < 0:
        raise HTTPException(status_code=400, detail="Resultado negativo!")

    return {"resultado": total, "WARNING": "Endpoint tem corpo de retorno mas utiliza método get."}



@app.post("/v1/soma_body", tags=[NomeGrupo.operacao], status_code=status.HTTP_200_OK)
def soma_body(num1: int, num2: int):

    if num1 < 0 or num2 < 0:
        raise HTTPException(status_code=400, detail="Não é permitido números negativos!")

    total = num1 + num2
    return {"resultado": total}



class Numero(BaseModel):
    numero1: int
    numero2: int

@app.post("/v1/soma_pydantic", tags=[NomeGrupo.operacao], status_code=status.HTTP_200_OK)
def soma_pydantic(num: Numero):
    total = num.numero1 + num.numero2
    return {"resultado": total}



class Resultado(BaseModel):
    resultado: int

@app.post("/v1/soma_com_response_model", response_model=Resultado, tags=[NomeGrupo.operacao], status_code=status.HTTP_200_OK)
def soma_response_model(num: Numero):
    total = num.numero1 + num.numero2
    return {"resultado": total}

@app.post("/v2/soma_com_response_model", tags=[NomeGrupo.operacao])
def soma_response_model_2(num: Numero) -> Resultado:
    total = num.numero1 + num.numero2
    return {"resultado": total}



class ResultadoFloat(BaseModel):
    resultado: float

@app.post("/v1/divisao", tags=[NomeGrupo.operacao])
def divisao(num: Numero) -> ResultadoFloat:

    if num.numero2 == 0:
        raise HTTPException(status_code=400, detail="Não é permitido divisão por 0!")
    
    total = num.numero1/num.numero2
    return {"resultado": total}


@app.post("/v1/soma_auth", tags=[NomeGrupo.operacao])
def soma_auth(num: Numero) -> Resultado:
    total = num.numero1 + num.numero2
    return {"resultado": total}

@app.post("/v1/get_api_key", tags=[NomeGrupo.texto])
def get_api_key(key: Auth):
    
    if key.dev_key != DEV_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Dev key não altorizada!")
    
    return {"api key": API_KEY}