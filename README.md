# WebWhisper

**WebWhisper** is a Streamlit-based web application that enables users to upload documents, perform semantic search across content, and get conversational answers using Groq's LLaMA-based models. It also supports PDF export of chat transcripts using WeasyPrint.

---

## 🚀 Features

- 📁 Upload and chunk documents (PDF, TXT, etc.)
- 🔍 Semantic search with embeddings
- 🤖 Conversational AI using Groq LLaMA models
- 📄 Export conversation to PDF

---

## 🛠️ Installation

1. **Clone the repository**
```bash
git clone https://github.com/your-username/WebWhisper.git
cd WebWhisper
```

2. **Create and activate a virtual environment**
```bash
python -m venv .venv
.venv\Scripts\activate    # On Windows
source .venv/bin/activate # On macOS/Linux
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `.env` file or export the variable:
```bash
$env:GROQ_API_KEY="sk-your-groq-api-key"  # Windows
export GROQ_API_KEY="sk-your-groq-api-key" # macOS/Linux
```

5. **Run the app**
```bash
streamlit run frontend/main.py
```

---

## 📦 Project Structure

```
WebWhisper/
│
├── .venv/                    # (Virtual environment folder)
│
├── app/
│   ├── __init__.py
│   ├── main.py               # Streamlit frontend entry point
│   ├── scraper.py            # Web scraping logic
│   ├── chunker.py            # Text chunking logic
│   ├── embedder.py           # Embedding + vector storage
│   ├── retriever.py          # Query + vector retrieval logic
│   ├── generator.py          # Call to Groq LLaMA-4 model
│   ├── pdf_exporter.py       # Markdown-to-PDF logic
│   └── utils.py              # Shared helper functions
│
├── frontend/                   # Streamlit app UI
│   └── main.py                 # Streamlit app entry point
│   
├── data/
│   └── vector_store/         # FAISS or ChromaDB files
│
├── requirements.txt          # Python dependencies
├── README.md                 # (Optional - project info)
└── .streamlit/
    └── config.toml           # Streamlit config (if needed)

```

## 📃 License
MIT License - feel free to use

---

## 🤝 Contributing
Pull requests are welcome! Open an issue first to discuss what you’d like to change.

---
