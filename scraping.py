from bs4 import BeautifulSoup

def scraping(s3, bucket_name):
    datos = []

    # Listamos todos los archivos en el bucket
    response = s3.list_objects_v2(Bucket=bucket_name)
    if "Contents" not in response:
        return datos  # No hay archivos en el bucket

    archivos_en_s3 = [obj["Key"] for obj in response["Contents"]]

    # Recorremos cada archivo para hacer scraping
    for archivo in archivos_en_s3:
        response = s3.get_object(Bucket=bucket_name, Key=archivo)
        contenido_html = response["Body"].read().decode("utf-8")
        soup = BeautifulSoup(contenido_html, "html.parser")
        listings = soup.find_all("div", class_="listing-card__content")

        for listing in listings:
            contenido = listing.find("div", class_="listing-card__information__main")
            if not contenido:
                continue  # Si no hay contenido, saltamos

            valor = contenido.find("span", class_="price__actual").text.strip() if contenido.find("span", class_="price__actual") else "N/A"
            barrio = contenido.find("div", class_="listing-card__location__geo").text.strip() if contenido.find("div", class_="listing-card__location__geo") else "N/A"

            # Buscar las propiedades
            propiedades = listing.find_all("div", class_=lambda x: x and "listing-card__properties__property" in x)
            
            momento = []
            for prop in propiedades:
                p_tags = prop.find_all("p")
                textos = [p.text.strip() for p in p_tags]
                momento.extend(textos)
            
            # Agrupar los textos en grupos de tres (o según la estructura que necesites)
            datos_agrupados = [", ".join(momento[i:i+3]) for i in range(0, len(momento), 3)]
            
            for grupo in datos_agrupados:
                datos.append([valor, barrio, grupo])

    return datos
