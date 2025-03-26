import os
import psycopg2
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

# Database Connection
DB_PARAMS = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

conn = psycopg2.connect(**DB_PARAMS)
cursor = conn.cursor()

# FAISS Storage Path
DB_FAISS_PATH = "vectorstore/db_faiss"

#Fetch Data from PostgreSQL
def fetch_data():
    cursor.execute("SELECT id, content FROM documents;")
    records = cursor.fetchall()
    return records

# Convert to Embeddings and Store in FAISS
def create_faiss_vectorstore():
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    records = fetch_data()

    documents = []
    for doc_id, content in records:
        doc = Document(page_content=content, metadata={"id": doc_id})
        documents.append(doc)

    # Use FAISS for Vector Storage
    faiss_db = FAISS.from_documents(documents, embedding_model)
    faiss_db.save_local(DB_FAISS_PATH)

    print(f" Stored {len(documents)} documents in FAISS.")

create_faiss_vectorstore()
conn.close()