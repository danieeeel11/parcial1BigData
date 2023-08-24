# parcial1BigData
Usergio - Parcial 1

1. Desarrollar un Pipeline de datos con AWS Lambda y Zappa para la descarga y procesamiento de información de los periódicos “eltiempo” y “el espectador”):
  a. Crear una lambda Zappa que descargue cada día la página principal del Tiempo y El Espectador(o publimetro).
    La información debe quedar en S3 con la estructura:
    s3://bucket/news/raw/contenido-yyyy-mm-dd.html
  b. Una vez llega el archivo a la carpeta raw, se debe activar un segundo Lambda que procese los datos que llegaron utilizando Beautifulsoup. Este proceso debe extraer la categoría, el titular y el enlace para cada noticia. Estos datos se deben     guardar en un csv en la siguiente ruta:
    s3://bucket/headlines/final/periodico=xxx/year=xxx/month=xxx/yyyy-mm-dd.csv
    Hay que crear un proyecto de zappa para cada función.
    Se debe entregar el código en github(utilizar ramas, commits, código limpio, código comentado.
    ** Se debe crear un Pipeline de despliegue continuo con Github actions que los siguientes pasos:
    Ejecución de flake 8
    Pruebas unitarias con pytest
    Desplegar con Zappa las funciones en AWS Lambda
