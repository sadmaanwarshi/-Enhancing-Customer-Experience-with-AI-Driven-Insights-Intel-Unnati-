import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint, HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from huggingface_hub import login
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()

app = FastAPI()

# CORS Middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# FAISS Storage Path
DB_FAISS_PATH = "vectorstore/db_faiss"

# Hugging Face API Token & Model
HF_TOKEN = os.getenv("HF_TOKEN")
HUGGINGFACE_REPO_ID = os.getenv("HUGGINGFACE_REPO_ID")

login(HF_TOKEN)

# Load LLM
def load_llm(huggingface_repo_id):
    return HuggingFaceEndpoint(
        repo_id=huggingface_repo_id,
        temperature=0.5,
        model_kwargs={"max_length": 512}
    )

# Custom Prompt Template
CUSTOM_PROMPT_TEMPLATE = """
Use the pieces of information provided in the context to answer user's question.
If you don't know the answer, just say that you don't know. 
Don't provide anything out of the given context.

Context: {context}
Question: {question}

Start the answer directly. No small talk please.
"""

def set_custom_prompt():
    return PromptTemplate(template=CUSTOM_PROMPT_TEMPLATE, input_variables=["context", "question"])

# Load FAISS Vectorstore
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)

# Create QA Chain
qa_chain = RetrievalQA.from_chain_type(
    llm=load_llm(HUGGINGFACE_REPO_ID),
    chain_type="stuff",
    retriever=db.as_retriever(search_kwargs={'k': 3}),
    return_source_documents=True,
    chain_type_kwargs={'prompt': set_custom_prompt()}
)

# Define Request Model
class QueryRequest(BaseModel):
    query: str

# API Endpoint to Handle Queries
@app.post("/ask")
async def ask_question(request: QueryRequest):
    try:
        response = qa_chain.invoke({'query': request.query})
        return {
            "response": response["result"],
            "source_documents": [doc.page_content for doc in response["source_documents"]]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {e}")

# Run the server using:
# uvicorn main:app --reload
