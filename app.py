import streamlit as st
import requests
import os

# Configura tu clave API de Cohere
API_KEY  = os.environ["COHERE_API_KEY"]

# URL de la API de Cohere
COHERE_API_URL = 'https://api.cohere.com/v1/chat'

# Función para enviar un mensaje a la API de Cohere
def send_message(message):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
    }
    data = {
        'preamble':
        """
        responde siempre de maner divertida y con emojis
        """,
        'message': message,
        'model': 'command-r-plus' 
    }
    response = requests.post(COHERE_API_URL, headers=headers, json=data)
    return response.json()

# Interfaz de usuario de Streamlit
st.title('Cohere Chat API Tester')

message = st.chat_input("Say something")

if message:
    with st.spinner("Esperando ..."):
        if message:
            response = send_message(message)
            if 'text' in response:
                st.write('Respuesta del modelo:')
                st.write(response['text'])
            else:
                st.write('No se recibió una respuesta válida.')
        else:
            st.write('Por favor, escribe un mensaje.')
