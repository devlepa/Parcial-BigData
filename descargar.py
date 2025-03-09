def archivos_s3_descargados(s3, bucket_name):
    """Lista y muestra el contenido de todos los archivos HTML almacenados en S3."""
    # Listar los archivos en el bucket
    response = s3.list_objects_v2(Bucket=bucket_name)

    if "Contents" not in response:
        print(f"⚠️ No hay archivos en el bucket '{bucket_name}'.")
        return {"status": "error", "message": "No hay archivos en el bucket."}

    archivos_en_s3 = [obj["Key"] for obj in response["Contents"]]
    print(f"📂 Archivos encontrados en '{bucket_name}':")
    for archivo in archivos_en_s3:
        print(f" - {archivo}")

    print(
        f"\n📄 Leyendo archivo y descargando archivos en local: {archivos_en_s3}")

    i = 0
    for archivo in archivos_en_s3:
        response = s3.get_object(Bucket=bucket_name, Key=archivo)
        html_content = response["Body"].read().decode("utf-8")
        with open(f"./html/index{i + 1}.html", "w") as file:
            file.write(html_content)
        i = i + 1

    return {
        "status": "success",
        "archivos_almacenados y guardados en local": archivos_en_s3}
