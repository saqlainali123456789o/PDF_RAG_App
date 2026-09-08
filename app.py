import streamlit as st
from config import APP_TITLE
from rag_pipeline import process_pdf, answer_question

st.set_page_config(page_title=APP_TITLE, page_icon="📚", layout="wide")

st.title("📚 PDF RAG Assistant")
st.caption("Upload a PDF, process it, and ask questions using Groq + FAISS.")

if "index" not in st.session_state:
    st.session_state.index = None
if "chunks" not in st.session_state:
    st.session_state.chunks = []
if "messages" not in st.session_state:
    st.session_state.messages = []

uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])

if uploaded_file:
    if st.button("Process PDF", type="primary"):
        with st.spinner("Extracting, chunking, embedding and indexing..."):
            try:
                index, chunks = process_pdf(uploaded_file)
                st.session_state.index = index
                st.session_state.chunks = chunks
                st.session_state.messages = []
                st.success(f"PDF processed successfully: {len(chunks)} chunks created.")
            except Exception as exc:
                st.error(f"Could not process the PDF: {exc}")

if st.session_state.index is not None:
    st.divider()
    st.subheader("Ask a question")

    question = st.text_input(
        "Question",
        placeholder="What is this document about?"
    )

    if st.button("Ask", type="primary"):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Searching the document and generating an answer..."):
                try:
                    answer, sources = answer_question(
                        question,
                        st.session_state.index,
                        st.session_state.chunks,
                    )

                    st.session_state.messages.append(
                        {"question": question, "answer": answer, "sources": sources}
                    )
                except Exception as exc:
                    st.error(f"Something went wrong: {exc}")

    for message in reversed(st.session_state.messages):
        st.markdown("### Question")
        st.write(message["question"])
        st.markdown("### Answer")
        st.write(message["answer"])

        if message["sources"]:
            st.markdown("**Sources**")
            for source in message["sources"]:
                st.write(f"- Page {source['page']} (chunk {source['chunk_id']})")
        st.divider()
else:
    st.info("Upload a PDF and click **Process PDF** to start.")
