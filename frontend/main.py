import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from app.scraper import scrape_website
from app.chunker import chunk_text
from app.embedder import create_embeddings, store_in_faiss
from app.retriever import retrieve
from app.generator import generate_response
from app.pdf_exporter import export_text_to_pdf
from sentence_transformers import SentenceTransformer

# Load embedding model once
embedder_model = SentenceTransformer("all-MiniLM-L6-v2")

# --- Theme Management ---
themes = {
    "Default": {"primary": "#4F8BF9", "background": "#FFFFFF", "text": "#000000"},
    "Dark": {"primary": "#1DB954", "background": "#121212", "text": "#FFFFFF"},
    "Solarized": {"primary": "#268BD2", "background": "#FDF6E3", "text": "#657B83"},
    "Dracula": {"primary": "#FF79C6", "background": "#282A36", "text": "#F8F8F2"},
    "Ocean": {"primary": "#00B8D4", "background": "#E0F7FA", "text": "#004D40"},
}

if "theme" not in st.session_state:
    st.session_state.theme = "Default"

theme = themes[st.session_state.theme]

def apply_theme(theme_dict):
    st.markdown(
        f"""
        <style>
            body, .stApp {{
                background-color: {theme_dict['background']};
                color: {theme_dict['text']};
            }}
            .stTextInput > div > div > input,
            .stButton > button {{
                background-color: {theme_dict['primary']}20;
                color: {theme_dict['text']};
                border: 1px solid {theme_dict['primary']};
                border-radius: 5px;
            }}
            .stTextInput > div > div > input::placeholder {{
                color: #aaa;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

apply_theme(theme)

# --- UI Layout ---
st.set_page_config(page_title="Chat with Website", layout="centered")
st.title("💬 Chat with Website")
st.markdown("Enter a website URL and ask questions based on its content.")

# Theme selector
st.sidebar.header("🎨 Theme Settings")
selected_theme = st.sidebar.selectbox("Choose Theme", options=list(themes.keys()), index=list(themes.keys()).index(st.session_state.theme))
if selected_theme != st.session_state.theme:
    st.session_state.theme = selected_theme
    st.experimental_rerun()

# Session state for chat
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

# --- Step 1: Website Input ---
st.subheader("🔗 Website")
url = st.text_input("Enter Website URL", placeholder="https://example.com")
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
    st.success("✅ Website processed and indexed!")

# --- Step 2: Query Input ---
if "index" in st.session_state:
    st.subheader("❓ Ask a Question")
    query = st.text_input("Your Question")

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
    st.subheader("📄 Export")
    if st.button("Download Chat as PDF"):
        combined_md = "\n\n---\n\n".join(st.session_state.chat_log)
        export_text_to_pdf(combined_md, "chat_output.pdf")
        with open("chat_output.pdf", "rb") as f:
            st.download_button("Download PDF", f, file_name="chat_output.pdf", mime="application/pdf")

