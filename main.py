import boto3
import pandas as pd
import datetime
import time
from fastapi import FastAPI

from verificar_crear import verificar_o_crear_bucket
from subir import subir_s3
from descargar import archivos_s3_descargados
from scraping import scraping

# Variables globales
path = "https://casas.mitula.com.co/casas/arriendo-bogota"
headers = {"user-Agent": "Mozilla/5.0"}
bucket_name_1 = "landing-casas-0101"
bucket_name_2 = "landing-casas-0101-processing"
date_str = datetime.datetime.now().strftime("%Y-%m-%d")
s3 = boto3.client("s3", region_name="us-east-1")

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Bienvenido a mi API"}


def crear_csv(datos):
    df = pd.DataFrame(datos, columns=["precio", "ubicacion", "detalles"])
    df.to_csv(f"./datos/datos{date_str}.csv")


def subir_csv_local(s3_client, local_csv_path, bucket_name, s3_key):
    s3_client.upload_file(local_csv_path, bucket_name, s3_key)
    print(f"Archivo '{local_csv_path}' subido a s3://{bucket_name}/{s3_key}")

# ------------------------------------------------------------------------
#  1) Lambda para descargar, scrapear y generar CSV
# ------------------------------------------------------------------------


def lambda_handler_download_scrape(event, context):

    # Verifica o crea bucket 1
    verificar_o_crear_bucket(bucket_name_1)
    time.sleep(2)

    # Sube HTMLs al bucket 1
    subir_s3(s3, path, headers, date_str, bucket_name_1)
    time.sleep(2)

    # Descarga HTMLs a local
    archivos_s3_descargados(s3, bucket_name_1)
    time.sleep(2)

    # Scrapear y crear CSV local
    datos_scrapeados = scraping(s3, bucket_name_1)
    crear_csv(datos_scrapeados)
    time.sleep(2)

    return {
        "status": "done",
        "message": "Datos descargados, scrapings realizados y CSV creado localmente."
    }

# ------------------------------------------------------------------------
#  2) Lambda para subir el CSV al segundo bucket
# ------------------------------------------------------------------------


def lambda_handler_upload_csv(event, context):
    s3 = boto3.client("s3", region_name="us-east-1")

    # Verifica o crea bucket 2
    verificar_o_crear_bucket(bucket_name_2)
    time.sleep(5)

    # Sube el CSV local al bucket 2
    local_csv_path = f"datos/datos{date_str}.csv"
    s3_key = f"carpeta/datos{date_str}.csv"

    subir_csv_local(s3, local_csv_path, bucket_name_2, s3_key)

    return {
        "status": "done",
        "message": f"Archivo {local_csv_path} subido a s3://{bucket_name_2}/{s3_key}"
    }


# ------------------------------------------------------------------------
#  Ejecución local con FastAPI (opcional)
# ------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    verificar_o_crear_bucket(bucket_name_1)
    time.sleep(2)

    # Sube HTMLs al bucket 1
    subir_s3(s3, path, headers, date_str, bucket_name_1)
    time.sleep(2)

    # Descarga HTMLs a local
    archivos_s3_descargados(s3, bucket_name_1)
    time.sleep(2)

    # Scrapear y crear CSV local
    datos_scrapeados = scraping(s3, bucket_name_1)
    crear_csv(datos_scrapeados)
    time.sleep(2)


    s3 = boto3.client("s3", region_name="us-east-1")

    # Verifica o crea bucket 2
    verificar_o_crear_bucket(bucket_name_2)
    time.sleep(5)

    # Sube el CSV local al bucket 2
    local_csv_path = f"datos/datos{date_str}.csv"
    s3_key = f"carpeta/datos{date_str}.csv"

    subir_csv_local(s3, local_csv_path, bucket_name_2, s3_key)

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
