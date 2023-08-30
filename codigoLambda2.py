import boto3
from bs4 import BeautifulSoup
# import csv
from datetime import datetime
# import io


def descargacsv():

    nombre = str(datetime.today().strftime('%Y-%m-%d'))
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('bucketparcial1')
    obj_tiempo = bucket.Object(str("news/raw/" +
                                   "eltiempo-" + nombre +
                                   ".html"))
    body_tiempo = obj_tiempo.get()['Body'].read()

    html_tiempo = BeautifulSoup(body_tiempo, 'html.parser')
    data_noticias_tiempo = html_tiempo.find_all('article')
    csv_tiempo = ""
    linea_0 = "Nombre; Categoria; Link\n"
    csv_tiempo += linea_0
    for i in range(len(data_noticias_tiempo)):
        link = "eltiempo.com" + \
               data_noticias_tiempo[i].find('a',
                                            class_='title page-link')['href']
        name = data_noticias_tiempo[i]['data-name'].replace(",", "")
        category = data_noticias_tiempo[i]['data-seccion']
        csv_tiempo += name + ";" + \
            category + ";" + \
            link + \
            "\n"

    boto3.client('s3').put_object(Body=csv_tiempo,
                                  Bucket='bucketparcial1',
                                  Key=str('headlines/final' +
                                          '/periodico=eltiempo/year=' +
                                          nombre[:4]+'-month=' +
                                          nombre[5:7]+'-day=' +
                                          nombre[8:]+'-eltiempo.csv'))

    obj_publimetro = bucket.Object(str("news/raw/" +
                                       "publimetro-" + nombre +
                                       ".html"))
    body_publimetro = obj_publimetro.get()['Body'].read()

    html_publimetro = BeautifulSoup(body_publimetro, 'html.parser')
    data_publimetro = html_publimetro.find_all('article')
    csv_publimetro = "" + linea_0
    for i in range(len(data_publimetro)):
        link = "publimetro.co" + \
               data_publimetro[i].find('a', class_='title page-link')['href']
        name = data_publimetro[i]['data-name'].replace(",", "")
        category = data_publimetro[i]['data-seccion']
        csv_publimetro += name + ";" + \
            category + ";" + \
            link + \
            "\n"

    boto3.client('s3').put_object(Body=csv_publimetro,
                                  Bucket='bucketparcial1',
                                  Key=str('headlines/final' +
                                          '/periodico=publimetro/year=' +
                                          nombre[:4]+'-month=' +
                                          nombre[5:7]+'-day=' +
                                          nombre[8:]+'-publimetro.csv'))


descargacsv()
