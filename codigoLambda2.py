import boto3
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import io


def descargacsv():
    # Configuración de Amazon S3
    s3 = boto3.client('s3')
    bucket_name = 'bucketparcial1'
    prefix = 'bucket/news/raw/'

    # Obtener la lista de objetos en el bucket
    objects = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

    # Procesar cada objeto
    for obj in objects.get('Contents', []):

        # Lista para almacenar los datos de las noticias
        news_data = []

        # Obtener el nombre del periódico del nombre del archivo
        newspaper_name = obj['Key'].split('-')[0]

        # Obtener el contenido del objeto HTML
        response = s3.get_object(Bucket=bucket_name, Key=obj['Key'])
        html_content = response['Body'].read()

        # Analizar el contenido HTML con Beautifulsoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extraer categoría, titular y enlace
        category = soup.find('meta', {'property': 'article:section'})['content']
        title = soup.find('title').get_text()
        link = soup.find('meta', {'property': 'og:url'})['content']

        # Agregar los datos a la lista
        news_data.append([category, title, link])

        # Generar la ruta del archivo CSV
        current_date = datetime.now().strftime('%Y-%m-%d')
        csv_key = (
            f'headlines/final/periodico={newspaper_name}/year={current_date[:4]}/'
            f'month={current_date[5:7]}/{current_date}.csv'
        )

        # Escribir los datos en el archivo CSV
        csv_buffer = io.StringIO()
        csv_writer = csv.writer(csv_buffer)
        csv_writer.writerow(['Categoría', 'Titular', 'Enlace'])
        csv_writer.writerows(news_data)

        # Subir el archivo CSV a S3
        s3.put_object(Body=csv_buffer.getvalue(), Bucket=bucket_name, Key=csv_key)

    print("Datos guardados en CSV en S3:", csv_key)

    return True
