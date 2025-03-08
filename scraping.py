import boto3
import pandas as pd
import datetime
from bs4 import BeautifulSoup
import requests




path = "https://casas.mitula.com.co/casas/arriendo-bogota"

s3_client = boto3.client("s3", "us-east-1")

headers = {"user-Agent": "Mozilla/5.0"}
response = requests.get(path, headers=headers)


if response.status_code == 200:
    for i in range(1, 11, 1):
        path = path + f"?page={i}"
        response = requests.get(path, headers=headers)
        with open(f"index{i}.html", "w", encoding="utf-8") as file:
            file.write(response.text)
    print("archivos guardados")
else:
    print("Error al acceder a la pagina", response.status_code)

for i in range(1, 11, 1):
    with open(f"./index{i}.html", "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
        section_houses = soup.find_all("div", class_="serp__main serp__main--no-dfp layout-padded")
        print(section_houses)


import boto3
import json

# Leer credenciales desde el archivo JSON
with open("aws_credentials.json", "r") as f:
    creds = json.load(f)

# Iniciar sesión con las credenciales temporales
session = boto3.Session(
    aws_access_key_id=creds["aws_access_key_id"],
    aws_secret_access_key=creds["aws_secret_access_key"],
    aws_session_token=creds["aws_session_token"],
    region_name=creds["region_name"]
)

# Cliente autenticado para S3
s3_client = session.client("s3")

# Listar los buckets disponibles
buckets = s3_client.list_buckets()
for bucket in buckets["Buckets"]:
    print(f"🔹 {bucket['Name']}")



