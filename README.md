# 🧹 Conversational RAG with PDF Uploads and Chat History

A Streamlit-based web app that allows users to upload PDF documents and interactively ask questions about their content using a Conversational Retrieval-Augmented Generation (RAG) pipeline powered by Groq LLMs and LangChain.

---

## 📊 Features
- Upload and chat with multiple PDF files.
- Conversational context-aware question reformulation.
- Uses Groq's ultra-fast LLMs via LangChain.
- HuggingFace Embeddings (MiniLM) for semantic understanding.
- Memory-based chat history support.
- Clean chat UI using Streamlit's new `chat_input` and `chat_message` features.

---

## 🚀 Tech Stack
- **Frontend/UI**: Streamlit
- **Backend / LLM Interface**: LangChain + ChatGroq (Gemma2-9b-It)
- **Vector Store**: ChromaDB
- **Embeddings**: HuggingFace (`all-MiniLM-L6-v2`)
- **PDF Parsing**: LangChain's PyPDFLoader
- **Session Management**: LangChain's `ChatMessageHistory`

---

## 📁 Project Structure
```
project/
├── app.py                # Main Streamlit application
├── requirements.txt      # Python dependencies
├── .env                  # Contains your HuggingFace API key
└── README.md             # This file
```

---

## 🚫 Prerequisites
Before running the app, ensure you have:

1. A **Groq API key**: https://console.groq.com/
2. A **HuggingFace API token** (for embeddings): https://huggingface.co/settings/tokens

---

## ⚙️ Installation & Setup

```bash
# 1. Clone the repository
https://github.com/yourusername/conversational-rag-pdf-chat.git
cd conversational-rag-pdf-chat

# 2. Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment variables
Create a `.env` file with the following content:
HUGGINGFACE_API=your_huggingface_token
```

---

## 🔄 Run the App

```bash
streamlit run app.py
```

Then, open the app in your browser at `http://localhost:8501`

---

## 🔧 How to Use
1. Paste your **Groq API key** in the input field.
2. Provide a **session ID** (any string).
3. Upload one or more **PDF files**.
4. Ask questions in the chat box about the uploaded content!

The app will:
- Parse and embed the content of uploaded PDFs.
- Build a vectorstore with ChromaDB.
- Use history-aware reformulation to make questions context-aware.
- Answer queries with context-aware responses.

---

## 🚨 Limitations
- No persistence: Uploaded PDFs and chat history are session-based.
- Limited to PDFs only (for now).
- You must bring your own Groq API key.

---

## 🚀 Future Enhancements
- Add sidebar to view previous sessions.
- Enable multi-format upload (e.g., DOCX, TXT).
- Download chat history.
- Cloud deployment (Streamlit Cloud, HuggingFace Spaces, etc).

---
