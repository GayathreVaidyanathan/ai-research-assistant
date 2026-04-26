# 🔬 AI Research Assistant

An intelligent research paper analysis tool that lets you upload any PDF research paper and chat with it using AI. Built with a RAG (Retrieval-Augmented Generation) pipeline powered by Groq and ChromaDB.

## Features
- 📄 Upload any PDF research paper
- 🤖 Auto-generates a summary of the paper on upload
- 💬 Chat with the paper — ask any question in plain English
- 🔍 RAG pipeline retrieves the most relevant sections before answering
- 📚 Maintains chat history within a session
- 🗑️ Clear and switch between papers easily
- 💡 Sample questions to get started quickly

## Tech Stack
| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| Backend | FastAPI + Uvicorn |
| Vector Store | ChromaDB |
| Embeddings | Sentence Transformers (all-MiniLM-L6-v2) |
| LLM | LLaMA 3.3 70B via Groq |
| PDF Parsing | PyMuPDF (fitz) |

## How It Works
1. PDF is uploaded and text is extracted using PyMuPDF
2. Text is chunked into 500-word segments with 50-word overlap
3. Chunks are embedded using Sentence Transformers and stored in ChromaDB
4. On each question, the top 5 most relevant chunks are retrieved
5. Retrieved context + question is sent to LLaMA 3.3 70B via Groq
6. Answer is returned with citations from the paper

## Getting Started

### Setup
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Environment Variables
Create a `.env` file:
GROQ_API_KEY=your_groq_api_key_here
Get a free API key at [console.groq.com](https://console.groq.com)

### Run Backend
```bash
uvicorn backend.main:app --reload --port 8000 --reload-exclude chroma_db
```

### Run Frontend
```bash
streamlit run frontend/app.py
```

Then open `http://localhost:8501` in your browser.

## Project Structure

ai-research-assistant/
├── backend/
│   ├── routers/
│   │   └── research.py      # API endpoints
│   ├── services/
│   │   ├── pdf_service.py       # PDF extraction and chunking
│   │   ├── embedding_service.py # ChromaDB and embeddings
│   │   └── llm_service.py       # Groq LLM calls
│   ├── main.py              # FastAPI app
│   └── config.py            # Settings
├── frontend/
│   └── app.py               # Streamlit UI
├── requirements.txt
└── .env

## Use Cases
- 📖 Quickly understand a research paper without reading it fully
- 🎓 Students reviewing papers for literature reviews
- 🔬 Researchers comparing methodologies across papers
- 💼 Professionals staying up to date with industry research
