import streamlit as st
import requests
import os
import fitz  # PyMuPDF

# Configura tu clave API de Cohere
API_KEY  = os.environ["COHERE_API_KEY"]

# URL de la API de Cohere
COHERE_API_URL = 'https://api.cohere.com/v1/chat'

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

# Interfaz de usuario de Streamlit
st.title('Cohere Chat API Tester')

uploaded_file = st.file_uploader("Sube un archivo PDF", type="pdf")
if uploaded_file:
    pdf_text = extract_text_from_pdf(uploaded_file)
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
else:
    st.write('Por favor, sube un archivo PDF.')
