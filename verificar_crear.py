import boto3

def verificar_o_crear_bucket(bucket_name):
    """Verifica si el bucket de S3 existe, si no, lo crea."""
    s3 = boto3.client("s3")

    buckets = [bucket["Name"] for bucket in s3.list_buckets().get("Buckets", [])]

    if bucket_name in buckets:
        print(f"✅ El bucket '{bucket_name}' ya existe.")
        return
    
    print(f"❌ El bucket '{bucket_name}' no existe. Creándolo...")

    s3.create_bucket(Bucket=bucket_name)
    print(f"✅ Bucket '{bucket_name}' creado exitosamente.")
    