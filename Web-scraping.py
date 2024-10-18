import requests
from lxml import html
import csv

# URL de la página que vamos a sacar toda la información
url = "https://WebEjemplo.com"  # Cambia esto por la URL real

# Encabezados para la solicitud HTTP
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Realizamos la solicitud HTTP con el método GET
response = requests.get(url, headers=headers)

# Comprobamos si la solicitud fue exitosa
if response.status_code == 200:
    # Parseamos el contenido de la página a string
    content = html.fromstring(response.content)

    # En esta línea debes de ajustar el patrón acorde a la web
    # Modifica esta línea según la estructura HTML de la página
    news_items = content.xpath('//div[@class="news-list-container"]//div[contains(@class, "news-item")]')  

    # Lista para almacenar los datos de las noticias
    news_data = []

    # Set para almacenar identificadores únicos (usaremos el enlace como ID)
    seen_links = set()

    # Recorremos cada noticia y extraemos la información
    for news_item in news_items:
        # Extraemos los datos
        categoria = news_item.xpath('.//span[contains(@class, "news-locator")]/text()')
        titulo = news_item.xpath('.//h3[contains(@class, "news-title")]/text()')
        autor = news_item.xpath('.//span[contains(@class, "news-author")]/text()')
        fecha = news_item.xpath('.//time[contains(@class, "news-time")]/text()')
        enlace = news_item.xpath('.//a/@href')
        imagen = news_item.xpath('.//img[contains(@class, "news-thumbnail")]/@src')

        # Usamos el enlace como identificador único
        if enlace:
            link = enlace[0]
            if link not in seen_links:  # Verificamos si el enlace ya fue procesado
                seen_links.add(link)  # Agregamos el enlace al conjunto

                # Agregamos la información de la noticia a la lista
                news_data.append({
                    'Categoría': categoria[0] if categoria else "N/A",
                    'Título': titulo[0] if titulo else "N/A",
                    'Autor': autor[0] if autor else "N/A",
                    'Fecha': fecha[0] if fecha else "N/A",
                    'Enlace': link,
                    'Imagen': imagen[0] if imagen else "N/A"
                })

    # Guardamos los datos en un archivo CSV
    with open('noticias.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Categoría', 'Título', 'Autor', 'Fecha', 'Enlace', 'Imagen']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(news_data)

    print("Información guardada en 'noticias.csv'")

else:
    print(f"Error al realizar la solicitud: {response.status_code}")


