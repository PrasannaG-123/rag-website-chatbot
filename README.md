# AI Website + PDF RAG Chatbot

A production-style AI chatbot that can:

- Read any website URL
- Extract website content
- Upload PDF documents
- Store text embeddings in FAISS Vector Database
- Answer user questions using Retrieval Augmented Generation (RAG)
- Maintain chat history with sidebar interface
- Provide real-time AI responses through FastAPI backend

This project simulates a real-world enterprise AI assistant.

---

# Project Demo

The chatbot can:

✔ Process Website URLs  
✔ Upload PDF documents  
✔ Ask questions from website content  
✔ Ask questions from uploaded PDF  
✔ Maintain chat history sidebar  
✔ Modern professional frontend UI  
✔ FastAPI backend APIs  
✔ FAISS vector database retrieval  

---

# Architecture

User Interface (HTML + CSS + JavaScript)

↓

FastAPI Backend

↓

Data Processing Layer

↓

Sentence Transformers Embedding Model

↓

FAISS Vector Database

↓

LLM (Gemini / OpenAI)

↓

Response Returned to Frontend

---

# Tech Stack Used

## Frontend

- HTML5
- CSS3
- JavaScript (Vanilla JS)

Purpose:

- Chat UI
- Sidebar history
- URL input
- PDF upload
- Ask question interface

---

## Backend Framework

- FastAPI

Purpose:

- API development
- Connecting frontend to backend
- Handling requests

APIs created:

```python
POST /process-url
POST /ask-question
POST /upload-pdf
```

---

## Web Scraping

- Requests
- BeautifulSoup4

Purpose:

Extract website content.

Example:

```python
response = requests.get(url)
soup = BeautifulSoup(response.text)
text = soup.get_text()
```

---

## PDF Processing

- PyMuPDF (fitz)

Purpose:

Read uploaded PDF documents.

Example:

```python
import fitz

doc = fitz.open("file.pdf")
text = ""

for page in doc:
    text += page.get_text()
```

---

## Text Splitting

- LangChain TextSplitter

Purpose:

Break large text into chunks before embedding.

Example:

```python
RecursiveCharacterTextSplitter
```

Why needed:

LLMs cannot process very long text directly.

---

## Embedding Model

- Sentence Transformers

Model used:

```python
all-MiniLM-L6-v2
```

Purpose:

Convert text into vector embeddings.

Example:

```python
SentenceTransformer("all-MiniLM-L6-v2")
```

Output:

```text
Text → 384 dimensional vector
```

---

## Vector Database

- FAISS

Purpose:

Store embeddings for similarity search.

Example:

```python
FAISS.from_texts()
```

Function:

When user asks a question:

```text
Find most relevant chunks
Return similar context
```

---

## Retrieval Augmented Generation (RAG)

RAG Pipeline:

```text
User Question

↓

Convert Question to Embedding

↓

Search Similar Vectors in FAISS

↓

Retrieve Relevant Chunks

↓

Send Context + Question to LLM

↓

Generate Answer
```

Purpose:

Make AI answer based on custom data instead of general knowledge.

---

## LLM Integration

Supported:

- Google Gemini API
- OpenAI API

Purpose:

Generate final answer using retrieved context.

Example:

```python
gemini.generate_content()
```

---

# Features Implemented

## Step 1

Basic FastAPI backend

Implemented:

```text
POST /process-url
POST /ask-question
```

---

## Step 2

Website scraping

Tools:

```text
Requests
BeautifulSoup
```

Implemented:

```text
Extract website text
```

---

## Step 3

Frontend chatbot UI

Tools:

```text
HTML
CSS
JavaScript
```

Implemented:

```text
URL input
Question input
Response output
```

---

## Step 4

Professional Chat UI

Implemented:

```text
Chat bubbles
Loading animation
Typing dots
Better styling
```

---

## Step 5

Sidebar Chat History

Implemented:

```text
New Chat button
Conversation sidebar
Multiple chat history cards
```

---

## Step 6

PDF Upload Support

Tools:

```text
python-multipart
PyMuPDF
```

API:

```python
POST /upload-pdf
```

Implemented:

```text
Upload PDF
Extract PDF text
Store in vector DB
```

---

## Step 7

Combined Knowledge Source

Implemented:

```text
Ask from website
Ask from uploaded PDF
Use same chatbot interface
```

Now chatbot supports:

```text
Website + PDF knowledge base
```

---

# APIs

## Process Website

Endpoint:

```text
POST /process-url
```

Input:

```json
{
  "url":"https://python.org"
}
```

---

## Ask Question

Endpoint:

```text
POST /ask-question
```

Input:

```json
{
  "question":"What is python?"
}
```

---

## Upload PDF

Endpoint:

```text
POST /upload-pdf
```

Input:

```text
multipart/form-data
```

Upload:

```text
file.pdf
```

---

# Installation

Clone repository

```bash
git clone YOUR_GITHUB_LINK
```

Create virtual environment

```bash
python -m venv .venv
```

Activate environment

```bash
.venv\Scripts\activate
```

Install requirements

```bash
pip install -r requirements.txt
```

Run backend

```bash
uvicorn backend_api:app --reload
```

Open frontend

```text
static/frontend/frontend.html
```

---

# Requirements

```txt
fastapi
uvicorn
langchain
faiss-cpu
sentence-transformers
beautifulsoup4
requests
python-multipart
pymupdf
google-genai
```

Install:

```bash
pip install -r requirements.txt
```

---

# Future Improvements

Planned upgrades:

- SQLite database
- User login system
- Persistent conversations
- Multi-user support
- Authentication
- Docker deployment
- AWS deployment
- Chat export
- Streamed AI response
- Authentication tokens
- Production hosting

---

# Learning Concepts Used

This project covers:

- Retrieval Augmented Generation
- API Development
- Frontend Development
- Vector Databases
- Embeddings
- Semantic Search
- LLM Integration
- FastAPI Development
- File Upload APIs
- PDF Processing
- Web Scraping
- AI System Design

---

# Author

Prasanna G

AI / Machine Learning Engineering Project

Built as real-world production style project.