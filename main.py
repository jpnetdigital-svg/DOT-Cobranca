import requests
import os 
import base64
import json
from datetime import datetime
from dotenv import load_dotenv

URL_BASE = "https://jpnetdigital.com.br/api/"

load_dotenv()
CLIENT_ID = os.getenv ("MK_CLIENT_ID")
CLIENT_SECRET = os.getenv("MK_CLIENT_SECRET")

if not CLIENT_ID or not CLIENT_SECRET:
    raise ValueError("Credênciais não Configuradas")

response = requests.get(
    URL_BASE, auth=(CLIENT_ID, CLIENT_SECRET)
)
response.raise_for_status()

TOKEN = response.text.strip()
print("Tamanho do token:", len(TOKEN))
print("partes do JWT:", TOKEN.count(".")+1)


payload = TOKEN.split(".")[1]
payload += "=" * (-len(payload) % 4)

dados_token = json.loads(
    base64.urlsafe_b64decode(payload).decode()
)

print("iat:", dados_token.get("iat"))
print("exp:", dados_token.get("exp"))

if dados_token.get("iat"):
    print("Emitido em:", datetime.fromtimestamp(dados_token["iat"]))

if dados_token.get("exp"):
    print("Expira em:", datetime.fromtimestamp(dados_token["exp"]))

print("Token JWT obtido com Sucesso!")

CPF = "86228635573"

URL_TITULOS = f"{URL_BASE}titulo/aberto/{CPF}"

headers = {"Authorization": f"Bearer {TOKEN}"}

response_titulos = requests.get(URL_TITULOS, headers=headers)

response_titulos.raise_for_status()

print("Titulos consultados com sucesso")
dados = response_titulos.json()

print(json.dumps(dados,indent=4, ensure_ascii=False))


