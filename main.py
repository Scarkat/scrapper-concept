import requests
from bs4 import BeautifulSoup
import os

def generar_misal():
    url = "https://misal.mx/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 1. Localizar el contenedor que vimos en tu imagen
        content_div = soup.find('div', class_='entry-content')
        if not content_div:
            print("No se encontró el contenido principal.")
            return

        # 2. Extraer las partes relevantes con FILTROS
        items_html = ""
        parrafos = content_div.find_all('p')

        # Definimos qué frases queremos ignorar
        innecesario = [
            "Con tu ayuda, podremos seguir manteniendo este sitio",
            "———-",
            "---"
        ]

        for p in parrafos:
            texto = p.get_text(strip=True)
            
            # FILTRO 1: Si el párrafo está vacío, saltar
            if not texto: 
                continue

            # FILTRO 2: Si el texto contiene alguna de nuestras frases basura, saltar
            # Usamos 'any' para revisar si alguna frase prohibida está dentro del texto
            if any(lines in texto for lines in innecesario):
                continue
 
            # Identificamos si es un título por la clase de fondo oscuro (image_b42cb5.png)
            clases = p.get('class', [])
            if 'has-very-dark-gray-background-color' in clases:
                items_html += f"<h2 style='color: #2c3e50; border-bottom: 2px solid #eee; padding-top: 15px;'>{texto}</h2>\n"
            else:
                items_html += f"<p style='line-height: 1.6; color: #333;'>{texto}</p>\n"

        # 3. Crear el template final
        html_completo = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>Misal del Día</title>
            <style>
                body {{ font-family: sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; background: #f9f9f9; }}
                .container {{ background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Misal del Día</h1>
                {items_html}
            </div>
        </body>
        </html>
        """

        # 4. Guardar en la carpeta output
        if not os.path.exists('output'): os.makedirs('output')
        
        with open("output/misal_hoy.html", "w", encoding="utf-8") as f:
            f.write(html_completo)
        
        print("¡Éxito! El archivo se ha generado en: output/misal_hoy.html")

    except requests.exceptions.HTTPError as err:
        print(f"Error del servidor: {err}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    generar_misal()