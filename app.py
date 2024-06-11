import streamlit as st
import requests
import os
import fitz  # PyMuPDF
from io import BytesIO

# Configura tu clave API de Cohere
API_KEY = os.environ["COHERE_API_KEY"]

# URL de la API de Cohere
COHERE_API_URL = 'https://api.cohere.com/v1/chat'

# Enlace directo del archivo PDF en el repositorio
PDF_URL = 'https://github.com/MargonDiego/ChatDemo/raw/main/REGLAMENTO%20INTERNO_RICE-2022.pdf'

# Función para enviar un mensaje a la API de Cohere
def send_message(message, context):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
    }
    data = {
        'preamble': "responde siempre de manera divertida y con emojis",
        'message': f"{context}\n\nPregunta: {message}",
        'model': 'command-r-plus'
    }
    response = requests.post(COHERE_API_URL, headers=headers, json=data)
    return response.json()

# Función para extraer texto del PDF
def extract_text_from_pdf(file):
    # Abre el archivo PDF desde un objeto BytesIO
    doc = fitz.open(stream=file, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Función para descargar un archivo desde una URL
def download_file_from_url(url):
    response = requests.get(url)
    response.raise_for_status()  # Asegúrate de que la solicitud fue exitosa
    return BytesIO(response.content)

# Interfaz de usuario de Streamlit
st.title('Cohere Chat API Tester')

with st.spinner("Descargando el PDF ..."):
    try:
        pdf_file = download_file_from_url(PDF_URL)
        pdf_text = extract_text_from_pdf(pdf_file)
        st.text_area("Contenido del PDF", pdf_text, height=200)
        
        message = st.chat_input("Pregunta algo sobre el PDF")
        if message:
            with st.spinner("Esperando ..."):
                response = send_message(message, pdf_text)
                if 'text' in response:
                    st.write('Respuesta del modelo:')
                    st.write(response['text'])
                else:
                    st.write('No se recibió una respuesta válida.')
    except Exception as e:
        st.write("Error al descargar o procesar el PDF:", str(e))
