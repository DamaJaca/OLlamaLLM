from ollama import chat
from ollama import ChatResponse
import pdfplumber
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
import os

model_id= 'deepseek-r1'

def solicitar_ruta_pdf():
    while True:
        ruta = input("Introduce la ruta del archivo a analizar: ").strip()

        # Verificar si el archivo existe
        if not os.path.isfile(ruta):
            print("Error: El archivo no existe. Inténtalo de nuevo.")
            continue

        # Verificar si la extensión es .pdf
        if not ruta.lower().endswith(".pdf"):
            print("Error: El archivo no es un PDF. Inténtalo de nuevo.")
            continue

        print("Archivo válido:", ruta)
        return ruta  # Devuelve la ruta válida

def cargar_pdf(path):
    texto = ""
    with pdfplumber.open(path) as pdf:
        for pagina in pdf.pages:
            texto += pagina.extract_text() +"\n"
    return texto


def responder_pregunta(pregunta, texto_documento):
    prompt = (
        "Utiliza el siguiente contexto para responder la pregunta:\n\n"
        f"{texto_documento}\n\n"
        f"Pregunta: {pregunta}"
    )
    response: ChatResponse = chat(model=model_id, messages=[
    {
        'role': 'user',
        'content': prompt
    },
    ])
    
    return response.message.content.split("</think>\n")[-1].strip()


def __main__():
    print("¡Hola! Estoy listo para responder preguntas sobre tu documento.")
    while True:
        pregunta = input("Hazme una pregunta sobre el documento o escribe \"salir\" para terminar el programa: ")
        if pregunta.lower() in ["salir", "exit"]:
            print("¡Hasta luego!")
            break
        respuesta = responder_pregunta("En el contexto del documento que te he pasado, responde: " + pregunta, documento_texto)
        print("Respuesta:", respuesta)



# Ejemplo de carga de PDF
ruta_pdf = solicitar_ruta_pdf()
documento_texto = cargar_pdf(ruta_pdf)
__main__()