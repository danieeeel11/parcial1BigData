import boto3
from bs4 import BeautifulSoup
# import csv
from datetime import datetime
# import io


def descargacsv():

    fecha = str(datetime.today().strftime('%Y-%m-%d'))
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('bucketparcial1')

    # Obtener el contenido HTML de El Tiempo
    obj_tiempo = bucket.Object("headlines/raw/eltiempo-" + fecha + ".html")
    body_tiempo = obj_tiempo.get()['Body'].read()
    html_tiempo = BeautifulSoup(body_tiempo, 'html.parser')
    data_noticias_tiempo = html_tiempo.find_all('article')

    # Obtener el contenido HTML de Publimetro
    obj_elespectador = bucket.Object("headlines/raw/elespectador-" 
                                     + fecha + ".html")
    body_elespectador = obj_elespectador.get()['Body'].read()
    html_elespectador = BeautifulSoup(body_elespectador, 'html.parser')
    data_noticias_elespectador = html_elespectador.find_all('article')

    # Generar los datos CSV para El Tiempo
    csv_tiempo = "Categoría, Titular, Enlace\n"
    for article in data_noticias_tiempo:
        link = "https://eltiempo.com" + 
            article.find('a', class_='title page-link')['href']
        category = article['data-seccion']
        title = article['data-name'].replace(",", "")
        csv_tiempo += f"{category}, {title}, {link}\n"

    # Generar los datos CSV para Publimetro
    csv_elespectador = "Categoría, Titular, Enlace\n"
    for article in data_noticias_elespectador:
        link = "https://elespectador.com" + article.find('a')['href']
        category = link.split('/')[3]
        title = article.find('a').text.replace(",", "")
        csv_elespectador += f"{category}, {title}, {link}\n"

    # Generar la ruta del archivo CSV y subirlo a S3
    csv_tiempo_key = (
        f'bucket/headlines/final/periodico=eltiempo/year={fecha[:4]}/'
        f'month={fecha[5:7]}/day={fecha[8:]}/eltiempo.csv'
    )
    csv_elespectador_key = (
        f'bucket/headlines/final/periodico=elespectador/year={fecha[:4]}/'
        f'month={fecha[5:7]}/day={fecha[8:]}/publimetro.csv'
    )

    s3_client = boto3.client('s3')
    s3_client.put_object(Body=csv_tiempo.encode('utf-8'), 
                         Bucket=bucket, 
                         Key=csv_tiempo_key)
    s3_client.put_object(Body=csv_elespectador.encode('utf-8'), 
                         Bucket=bucket, 
                         Key=csv_elespectador_key)

    print("Archivos CSV generados y subidos a S3.")
    return True
