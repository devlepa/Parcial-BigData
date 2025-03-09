import requests

def subir_s3(s3, path, headers, date_str, bucket_name):
    """Descarga archivos .html de Mitula y los sube a S3."""
    descargados = 0
    for i in range(1, 11, 1):
        url = f"{path}?page={i}"
        response = requests.get(url, headers=headers)
        file_name = f"{date_str}index{i}.html"

        s3.put_object(Bucket=bucket_name, Key=file_name, Body=response.text)
        descargados += 1
        print(f"✅ Archivo subido a S3: s3://{bucket_name}/{file_name}")
    