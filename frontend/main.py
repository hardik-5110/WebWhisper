import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
from app.scraper import scrape_website
from app.chunker import chunk_text
from app.embedder import create_embeddings, store_in_faiss
from app.retriever import retrieve
from app.generator import generate_response
from app.pdf_exporter import export_chat_to_pdf
from sentence_transformers import SentenceTransformer
import os

# Load embedding model once
embedder_model = SentenceTransformer("all-MiniLM-L6-v2")

# Session state for chat
if 'chat_log' not in st.session_state:
    st.session_state.chat_log = []

st.set_page_config(page_title="Chat with Website", layout="centered")

st.title("💬 Chat with Website")
st.markdown("Enter a website URL and ask questions based on its content.")

# --- Step 1: Website Input ---
url = st.text_input("🔗 Enter Website URL", placeholder="https://example.com")
process_btn = st.button("Process Website")

if process_btn and url:
    with st.spinner("Scraping and processing website..."):
        raw_text = scrape_website(url)
        chunks = chunk_text(raw_text)
        embeddings = create_embeddings(chunks)
        index, stored_chunks = store_in_faiss(embeddings, chunks)

    st.session_state.raw_text = raw_text
    st.session_state.index = index
    st.session_state.chunks = stored_chunks
    st.success("Website processed and indexed!")

# --- Step 2: Query Input ---
if 'index' in st.session_state:
    query = st.text_input("❓ Ask a question based on the website content")

    if st.button("Get Answer") and query:
        with st.spinner("Retrieving relevant content and generating response..."):
            relevant_chunks = retrieve(query, embedder_model, st.session_state.index, st.session_state.chunks)
            response = generate_response(query, relevant_chunks)

            # Display response
            st.markdown("### 🤖 Answer")
            st.markdown(f"<div style='text-align: justify'>{response}</div>", unsafe_allow_html=True)

            # Show reference chunks
            with st.expander("📎 Reference Chunks"):
                for i, chunk in enumerate(relevant_chunks, 1):
                    st.markdown(f"**Chunk {i}:**\n> {chunk[:500]}...")

            # Log chat
            st.session_state.chat_log.append(f"**User**: {query}\n\n**AI**: {response}")

# --- Step 3: Download PDF ---
if st.session_state.chat_log:
    if st.button("📄 Download Chat as PDF"):
        combined_md = "\n\n---\n\n".join(st.session_state.chat_log)
        export_chat_to_pdf(combined_md, "chat_output.pdf")
        with open("chat_output.pdf", "rb") as f:
            st.download_button("Download PDF", f, file_name="chat_output.pdf", mime="application/pdf")
