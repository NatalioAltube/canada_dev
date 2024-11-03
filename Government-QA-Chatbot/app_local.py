from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain.schema import Document
import fitz  # PyMuPDF para manejar PDFs
import openai
import faiss
import numpy as np

openai.api_key = 'YOUR_API_KEY_HERE'

# Función para configurar la clave de API en OpenAIEmbeddings
def configurar_openai_embeddings():
    try:
        print("Cargando modelo de embeddings de OpenAI...")
        # Ajusta la creación de OpenAIEmbeddings para que funcione correctamente
        embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=openai.api_key)
        print("Modelo de embeddings cargado exitosamente.")
        return embeddings
    except Exception as e:
        print(f"Error al configurar OpenAIEmbeddings: {e}")
        raise

# Cargar PDFs y extraer texto
def cargar_pdfs(ruta_pdfs):
    textos = []
    for pdf in ruta_pdfs:
        try:
            print(f"Procesando {pdf}...")
            documento = fitz.open(pdf)
            texto_pdf = ""
            for pagina in documento:
                texto_pdf += pagina.get_text()
            textos.append(texto_pdf)
        except Exception as e:
            print(f"Error al abrir {pdf}: {e}")
    return textos

# Fragmentar texto en trozos más pequeños
def fragmentar_texto(texto, max_tokens=500):
    palabras = texto.split()
    fragmentos = []
    while len(palabras) > 0:
        fragmento = " ".join(palabras[:max_tokens])
        fragmentos.append(fragmento)
        palabras = palabras[max_tokens:]
    return fragmentos

# Procesar embeddings por lotes e inicializar FAISS correctamente
def procesar_embeddings_por_lotes(fragmentos, embedding_model, batch_size=10):
    dimension_embedding = np.array(embedding_model.embed_documents(["test"])).shape[1]
    index = faiss.IndexFlatL2(dimension_embedding)
    docstore = InMemoryDocstore({})
    index_to_docstore_id = {}

    for i in range(0, len(fragmentos), batch_size):
        batch = fragmentos[i:i + batch_size]
        embeddings = np.array(embedding_model.embed_documents(batch))
        index.add(embeddings)
        for idx, fragment in enumerate(batch):
            doc_id = len(index_to_docstore_id)
            index_to_docstore_id[doc_id] = doc_id
            docstore._dict[doc_id] = Document(page_content=fragment)

    vectorstore = FAISS(embedding_function=embedding_model, index=index, docstore=docstore, index_to_docstore_id=index_to_docstore_id)
    return vectorstore

# Lista de archivos PDF
pdf_files = [
    "pdf/secu_-_december_16,_2021.pdf",
    "pdf/secu_-_july_25,_2022.pdf",
]

# Extraer y fragmentar texto de los archivos PDF
textos_documentos = cargar_pdfs(pdf_files)
fragmentos = [fragmento for texto in textos_documentos for fragmento in fragmentar_texto(texto)]

# Cargar modelo de embeddings correctamente
embeddings = configurar_openai_embeddings()

# Procesar los embeddings por lotes
print("Procesando los embeddings por lotes...")
vectorstore = procesar_embeddings_por_lotes(fragmentos, embeddings)

# Configuración de FastAPI
app = FastAPI()

# Clase para recibir las preguntas en JSON
class Question(BaseModel):
    pregunta: str

# Función para generar respuestas con OpenAI GPT-4 usando el endpoint de chat
def generar_respuesta(contexto, pregunta):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Context: {contexto}\n\nQuestion: {pregunta}"}
    ]
    try:
        print("Generando respuesta con OpenAI...")
        print(f"Contexto: {contexto[:500]}")  # Muestra los primeros 500 caracteres para depuración
        print(f"Pregunta: {pregunta}")
        respuesta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            max_tokens=150,
            temperature=0
        )
        print("Respuesta generada con éxito.")
        return respuesta.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Error en la generación de respuesta: {e}")
        return "Hubo un error al procesar la respuesta."

# Endpoint para recibir preguntas y dar respuestas
@app.post("/preguntar")
async def preguntar(question: Question):
    try:
        print(f"Recibida pregunta: {question.pregunta}")
        print("Buscando contexto relevante usando similarity_search...")
        docs = vectorstore.similarity_search(question.pregunta, k=1)
        if not docs or not docs[0]:
            raise ValueError("No se encontraron documentos relevantes.")
        context = docs[0].page_content
        print(f"Contexto relevante encontrado: {context[:500]}")
        respuesta = generar_respuesta(context, question.pregunta)
        print(f"Respuesta generada: {respuesta}")
        return {"respuesta": respuesta}
    except Exception as e:
        print(f"Error procesando la respuesta: {e}")
        raise HTTPException(status_code=500, detail=f"Error procesando la respuesta: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)