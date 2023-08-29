import boto3
import urllib.request
from datetime import datetime

def lambda_handler(event, context):

    # Definir URLs de los periódicos
    urls = {
        "eltiempo": "https://www.eltiempo.com/",
        "elespectador": "https://www.elespectador.com/"
    }

    # Configurar cliente de S3
    s3_client = boto3.client("s3")
    
    # Obtener fecha actual
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    for newspaper, url in urls.items():
    
        response = urllib.request.urlopen(url)
        
	content = response.read()
	    
	# Definir la ruta en S3
	s3_path = f"bucket/news/raw/{newspaper}/{current_date}.html"
	    
	# Subir contenido a S3
	s3_client.put_object(Bucket="bucketparcial1", Key=s3_path, Body=content)
	    
	print(f"Contenido de {newspaper} guardado en S3: {s3_path}")
	    
	return {
	   'statusCode': 200,
	   'body': 'Página del tiempo descargada y subida exitosamente a S3.'	
	}