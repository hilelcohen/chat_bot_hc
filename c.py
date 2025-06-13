import streamlit as st
import groq

def configurar_pagina():
    st.set_page_config(page_title="MI PRIMERA PAGINA CON PYTHON", page_icon="😀")
    st.title("Bienvenidos a mi chatbot")

MODELOS=['11ama3-8b-8192','1lama3-79b-8192','mixtral-8x7b-32768']

def mostrar_sidebar():
    st.sidebar.title("ELEJÍ TU MODELO DE IA FAVORITO")
    modelo=st.sidebar.selectbox("¿ Cuál elejís ?" , MODELOS , index=2)
    st.write(f"*ELEJISTE EL MODELO*: {modelo}")
    return modelo


def crear_cliente_groq():
    groq_api_key = st.secrets["GROQ_API_KEY"]
    return groq.Groq(api_key=groq_api_key)

    #INICIALIAR EL ESTADO DE LOS MENSAJE
def inicializacion_estado_chat():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

# HISTORIAL DEL CHAT
def mostrar_historial_chat():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"]):  #context manager 
            st.markdown(mensaje["content"])


def obtener_mensaje_usuario():
    return st.chat_input("Envia un mensaje")

# AGREGAR LOS MENSAJE AL ESTADO
def agregar_mensaje_al_historial(role, content):
    st.session_state.mensajes.append({"role":role, "content":content})

# MOSTRAR LOS MENSAJES EN PANTALLA
def  mostrar_mensaje(role, content):
     with st.chat_message(role):
        st.markdown(content)

# LLAMAR AL MODELO DE GROQ
def obtener_respuesta_modelo(cliente, modelo, mensajes):
    respuesta = cliente.chat.completions.create(
        model=modelo,
        messages=mensajes,
        stream = False
    )
    return respuesta.choices[0].message.content
    
    
def ejecutar_app():
    configurar_pagina()
    mostrar_sidebar()
    

    inicializacion_estado_chat()
    mensaje_usuario = obtener_mensaje_usuario()

    if mensaje_usuario :
        agregar_mensaje_al_historial("user",mensaje_usuario)
        mostrar_mensaje("user",mensaje_usuario)

def ejecutar_app():
    configurar_pagina()
    modelo = mostrar_sidebar()
    inicializacion_estado_chat()
    mostrar_historial_chat()
    
    mensaje_usuario = obtener_mensaje_usuario()

    if mensaje_usuario:
        agregar_mensaje_al_historial("user", mensaje_usuario)
        mostrar_mensaje("user", mensaje_usuario)

        cliente = crear_cliente_groq()
        respuesta = obtener_respuesta_modelo(cliente, modelo, st.session_state.mensajes)

        agregar_mensaje_al_historial("assistant", respuesta)
        mostrar_mensaje("assistant", respuesta)


    
if __name__ == '__main__' :
    ejecutar_app()