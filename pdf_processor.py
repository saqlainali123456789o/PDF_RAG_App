import re
import fitz


def extract_pages(pdf_file):
    """Extract text page-by-page and preserve page numbers."""
    pdf_bytes = pdf_file.getvalue()
    document = fitz.open(stream=pdf_bytes, filetype="pdf")

    pages = []
    for page_number, page in enumerate(document, start=1):
        text = page.get_text("text")
        if text and text.strip():
            pages.append({
                "page": page_number,
                "text": text.strip()
            })

    document.close()
    return pages


def clean_text(text):
    """Normalize unnecessary whitespace without destroying content."""
    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def build_chunks(pages, chunk_size=800, overlap=100):
    """
    Character-based chunking for a simple first RAG version.
    Page metadata is preserved for source display.
    """
    if overlap >= chunk_size:
        raise ValueError("CHUNK_OVERLAP must be smaller than CHUNK_SIZE.")

    chunks = []
    chunk_id = 0

    for page in pages:
        text = clean_text(page["text"])
        if not text:
            continue

        start = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append({
                    "text": chunk_text,
                    "page": page["page"],
                    "chunk_id": chunk_id
                })
                chunk_id += 1

            if end >= len(text):
                break

            start = end - overlap

    return chunks
