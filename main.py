import boto3
import pandas as pd
import datetime
import time

from verificar_crear import verificar_o_crear_bucket
from subir import subir_s3
from descargar import archivos_s3_descargados
from scraping import scraping

path = "https://casas.mitula.com.co/casas/arriendo-bogota"
headers = {"user-Agent": "Mozilla/5.0"}
bucket_name_1 = "landing-casas-0101"
bucket_name_2 = "landing-casas-0101-processing"
s3 = boto3.client("s3", region_name="us-east-1")
date_str = datetime.datetime.now().strftime("%Y-%m-%d")

    
  
def crear_csv(datos):
    
    df = pd.DataFrame(datos, columns=["precio", "ubicacion", "detalles"])
    df.to_csv("./datos/datos.csv")


def lambda_handler(event, context):
    """
    Función Lambda que ejecuta la descarga y procesamiento de datos en AWS.
    Se ejecuta automáticamente cada lunes a las 9 AM.
    """

    verificar_o_crear_bucket(bucket_name_1)

    subir_s3(s3, path, headers, date_str, bucket_name_1)

    archivos_s3_descargados()

    crear_csv(scraping())





if '__main__' == __name__:
    verificar_o_crear_bucket(bucket_name=bucket_name_1)
    #time.sleep(10)
    subir_s3(s3, path, headers, date_str, bucket_name_1)
    #time.sleep(10)
    crear_csv(scraping(s3, bucket_name_1))
    #time.sleep(10)
    