# AI Customer Experience Chatbot

This project is an AI-powered customer experience chatbot that enables businesses to connect their own large database with an advanced conversational model. The chatbot is designed to provide users with relevant answers to their queries by retrieving context-aware responses from a stored vector database using FAISS and an LLM (Large Language Model) hosted on Hugging Face.

## Features
- Seamless integration with any large document or product database.
- Uses **FAISS** for efficient vector search.
- Employs **Hugging Face's Mistral-7B-Instruct-v0.3** model for answering user queries.
- **FastAPI** backend for handling chatbot requests.
- Supports environment variables for security.
- Fully functional API that can be integrated into any frontend.

## Tech Stack
- **Backend**: FastAPI, Python
- **Vector Database**: FAISS
- **Embeddings**: Hugging Face Embeddings (`sentence-transformers/all-MiniLM-L6-v2`)
- **LLM**: Hugging Face Mistral-7B
- **Frontend**: (Optional, can be integrated with any frontend framework)
- **Database**: PostgreSQL (if needed for structured data storage)

---

## Installation & Setup

### 1. Clone the Repository
```bash
 git clone https://github.com/sadmaanwarshi/-Enhancing-Customer-Experience-with-AI-Driven-Insights-Intel-Unnati-.git
 cd your-repo-name
```

### 2. Set Up a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate    # On Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Environment Variables Setup
Create a `.env` file in the project root and add the following:
```ini
HF_TOKEN=your_huggingface_api_token
DB_FAISS_PATH=vectorstore/db_faiss
DB_NAME=e-commerce-model
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

Load environment variables automatically:
```bash
export $(cat .env | xargs)
```
---

## **Step 1: Storing Embeddings**
Before running the chatbot, you need to generate and store vector embeddings from your dataset into FAISS.

Run the script:
```bash
python store_embedding.py
```
This will:
- Convert your documents into vector embeddings.
- Store them in FAISS for fast retrieval.

---

## **Step 2: Running the Backend**
Start the FastAPI server:
```bash
uvicorn main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

### API Endpoint
- `POST /ask`: Ask a question and get a relevant response.

Example:
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/ask' \
  -H 'Content-Type: application/json' \
  -d '{"query": "What is a good laptop for gaming?"}'
```
---

## **Step 3: Connecting to the Frontend**
You can integrate this API into any frontend framework (React, Vue, etc.).

Example: Making a request from a React frontend:
```javascript
fetch("http://127.0.0.1:8000/ask", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ query: "What is the best smartphone?" })
})
.then(response => response.json())
.then(data => console.log(data.response));
```

---

## **How It Works**
1. **Embedding Storage**: 
   - The system converts your dataset into numerical vectors using `sentence-transformers/all-MiniLM-L6-v2`.
   - The embeddings are stored in FAISS for efficient retrieval.

2. **Query Processing**:
   - When a user asks a question, the bot retrieves the most relevant embeddings from FAISS.
   - The retrieved data is sent to the **Mistral-7B-Instruct-v0.3** model.
   - The model generates a context-aware response based on retrieved data.

3. **Response Generation**:
   - The chatbot responds with relevant answers only based on the stored knowledge.
   - If the answer is unknown, it politely states it does not have enough information.

---

## **Use Case: AI-Powered Customer Support**
- Businesses can connect their product database with this chatbot to provide instant customer support.
- Users can ask questions about product specifications, availability, and usage.
- Enhances customer engagement and reduces human support workload.

---

## Future Enhancements
- Implement **database connectivity** for structured queries.
- Support **multi-language models** for broader reach.
- Add **user authentication** to personalize responses.
- Enable **voice-to-text** interaction for hands-free queries.

---

## Contributing
Feel free to fork this repository, make changes, and submit a pull request!

## License
This project is open-source and available under the MIT License.

---

### **Author**
Developed by **Sadmaan Warshi** 🚀
