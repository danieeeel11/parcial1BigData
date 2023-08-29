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
                                  Key=str('bucket/headlines/final' +
                                          '/periodico=eltiempo/year=' +
                                          nombre[:4]+'-month=' +
                                          nombre[5:7]+'-day=' +
                                          nombre[8:]+'-eltiempo.csv'))

    obj_espectador = bucket.Object(str("news/raw/" +
                                   "elespectador-" + nombre +
                                   ".html"))
    body_espectador = obj_espectador.get()['Body'].read()

    html_espectador = BeautifulSoup(body_espectador, 'html.parser')
    data_noticias_espectador = html_tiempo.find_all('article')
    csv_espectador = ""
    
    for i in range(len(data_noticias_espectador)):
        link = "elespectador.com" + \
               data_noticias_espectador[i].find('a',
                                            class_='title page-link')['href']
        name = data_noticias_espectador[i]['data-name'].replace(",", "")
        category = data_noticias_espectador[i]['data-seccion']
        csv_espectador += name + ";" + \
            category + ";" + \
            link + \
            "\n"

    boto3.client('s3').put_object(Body=csv_espectador,
                                  Bucket='bucketparcial1',
                                  Key=str('bucket/headlines/final' +
                                          '/periodico=elespectador/year=' +
                                          nombre[:4]+'-month=' +
                                          nombre[5:7]+'-day=' +
                                          nombre[8:]+'-elespectador.csv'))
    
    return True
