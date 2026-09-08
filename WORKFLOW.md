# Development Workflow

## Phase 1
Create the project and virtual environment.

## Phase 2
Test PDF extraction:
PDF -> page text.

## Phase 3
Test cleaning:
raw text -> cleaned text.

## Phase 4
Test chunking:
cleaned text -> overlapping chunks + page metadata.

## Phase 5
Test embeddings:
chunks -> vectors.

## Phase 6
Test FAISS:
vectors -> searchable index.

## Phase 7
Test retrieval:
question -> top-K relevant chunks.

## Phase 8
Test Groq:
context + question -> grounded answer.

## Phase 9
Combine everything in rag_pipeline.py.

## Phase 10
Run Streamlit UI.

## Phase 11
Add session state, source display, and error handling.

## Phase 12
Test locally.

## Phase 13
Push safe files to GitHub.

## Phase 14
Deploy to Streamlit Community Cloud and configure secrets.

## Testing checklist
- [ ] PDF extracts correctly
- [ ] Chunks are created
- [ ] Embeddings work
- [ ] FAISS index is created
- [ ] Relevant chunks are retrieved
- [ ] Groq answer is generated
- [ ] Sources show page numbers
- [ ] Missing API key gives a useful error
- [ ] .env is not committed
- [ ] App runs on Streamlit
