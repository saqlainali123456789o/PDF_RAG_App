# 📚 PDF RAG Assistant

A Retrieval-Augmented Generation (RAG) application built with Python, Streamlit, FAISS, Sentence Transformers, and Groq.

## Features

- Upload a PDF
- Extract text page-by-page
- Clean and chunk document text
- Create open-source embeddings
- Store vectors in FAISS
- Retrieve relevant chunks for a question
- Generate grounded answers using Groq
- Display source page numbers
- Keep the FAISS index in Streamlit session state

## Architecture

PDF → PyMuPDF → Cleaning → Chunking → Embeddings → FAISS

Question → Embedding → FAISS Retrieval → Context → Groq → Answer

## Project Structure

```text
PDF_RAG_App/
├── app.py
├── config.py
├── pdf_processor.py
├── embeddings.py
├── vector_store.py
├── rag_pipeline.py
├── prompts.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── data/
    └── uploads/
```

## Local Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd PDF_RAG_App
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Groq

Copy `.env.example` to `.env`:

```text
GROQ_API_KEY=your_real_key
GROQ_MODEL=llama-3.1-8b-instant
```

Never upload `.env` to GitHub.

### 5. Run

```bash
streamlit run app.py
```

## RAG Workflow

1. User uploads PDF.
2. PyMuPDF extracts page text.
3. Text is cleaned.
4. Text is divided into overlapping chunks.
5. Sentence Transformer creates embeddings.
6. FAISS stores vectors.
7. User asks a question.
8. The question is embedded.
9. FAISS retrieves top-K chunks.
10. Retrieved chunks become the context.
11. Groq generates a grounded answer.
12. The application displays the answer and source pages.

## Important Notes

This first version is intentionally simple. It uses an in-memory FAISS index per Streamlit session. It is not a multi-user persistent document database.

Scanned PDFs may require OCR. Retrieval quality can be improved later with better chunking, metadata filtering, reranking, hybrid search, and evaluation.

## Deployment

Deploy `app.py` using Streamlit Community Cloud.

Configure the secret in Streamlit:

```toml
GROQ_API_KEY = "your_real_key"
GROQ_MODEL = "llama-3.1-8b-instant"
```

Do not commit API keys to the repository.
