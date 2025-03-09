import boto3
import pandas as pd
import datetime
import time

from verificar_crear import verificar_o_crear_bucket
from subir import subir_s3
from descargar import archivos_s3_descargados
from scraping import scraping
from fastapi import FastAPI

path = "https://casas.mitula.com.co/casas/arriendo-bogota"
headers = {"user-Agent": "Mozilla/5.0"}
bucket_name_1 = "landing-casas-0101"
bucket_name_2 = "landing-casas-0101-processing"
s3 = boto3.client("s3", region_name="us-east-1")
date_str = datetime.datetime.now().strftime("%Y-%m-%d")


app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Bienvenido a mi API"}


def crear_csv(datos):

    df = pd.DataFrame(datos, columns=["precio", "ubicacion", "detalles"])
    df.to_csv(f"./datos/datos{date_str}.csv")


def subir_csv_local(s3_client, local_csv_path, bucket_name, s3_key):
    """
    Sube un archivo CSV local a S3.
    """
    s3_client.upload_file(local_csv_path, bucket_name, s3_key)
    print(f"Archivo '{local_csv_path}' subido a s3://{bucket_name}/{s3_key}")


if '__main__' == __name__:
    import uvicorn
    verificar_o_crear_bucket(bucket_name=bucket_name_1)
    time.sleep(10)
    subir_s3(s3, path, headers, date_str, bucket_name_1)
    time.sleep(10)
    archivos_s3_descargados(s3, bucket_name_1)
    time.sleep(10)
    crear_csv(scraping(s3, bucket_name_1))
    time.sleep(10)
    verificar_o_crear_bucket(bucket_name=bucket_name_2)
    time.sleep(10)
    s3 = boto3.client('s3', region_name='us-east-1')
    subir_csv_local(
        s3_client=s3,
        local_csv_path=f"datos/datos{date_str}.csv",
        bucket_name=bucket_name_2,
        s3_key=f"carpeta/datos{date_str}.csv"
    )
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
