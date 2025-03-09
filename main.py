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
    df.to_csv("./datos/datos.csv")


if '__main__' == __name__:
    import uvicorn
    verificar_o_crear_bucket(bucket_name=bucket_name_1)
    time.sleep(10)
    subir_s3(s3, path, headers, date_str, bucket_name_1)
    time.sleep(10)
    crear_csv(scraping(s3, bucket_name_1))
    time.sleep(10)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
