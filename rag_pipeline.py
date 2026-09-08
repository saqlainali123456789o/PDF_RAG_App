from groq import Groq

from config import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    GROQ_API_KEY,
    GROQ_MODEL,
    TOP_K,
)
from pdf_processor import build_chunks, extract_pages
from prompts import build_prompt
from vector_store import create_index, search_index


def process_pdf(pdf_file):
    pages = extract_pages(pdf_file)

    if not pages:
        raise ValueError(
            "No readable text was found. This may be a scanned/image-only PDF."
        )

    chunks = build_chunks(
        pages,
        chunk_size=CHUNK_SIZE,
        overlap=CHUNK_OVERLAP
    )

    if not chunks:
        raise ValueError("No text chunks were created from the PDF.")

    index = create_index(chunks)
    return index, chunks


def _get_groq_client():
    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY is missing. Add it to .env locally or Streamlit Secrets in deployment."
        )

    return Groq(api_key=GROQ_API_KEY)


def answer_question(question, index, chunks):
    retrieved = search_index(
        question,
        index,
        chunks,
        top_k=TOP_K
    )

    if not retrieved:
        return "I could not find relevant information in the uploaded document.", []

    context_parts = []
    for item in retrieved:
        context_parts.append(
            f"[Page {item['page']} | Chunk {item['chunk_id']}]\n{item['text']}"
        )

    context = "\n\n".join(context_parts)
    prompt = build_prompt(context, question)

    client = _get_groq_client()

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=1000,
    )

    answer = response.choices[0].message.content.strip()

    return answer, retrieved
