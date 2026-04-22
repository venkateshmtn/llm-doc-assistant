# 📄 Chat with PDF using LLM

An AI-powered application that allows users to upload a PDF and ask questions about its content using Large Language Models (LLMs).

---

## 🚀 Features

- 📂 Upload any PDF document
- 🔍 Semantic search using vector embeddings (FAISS)
- 💬 Ask questions about the document
- 🧠 Extract key skills automatically
- 📝 Generate professional summary
- 📊 Identify experience from resume
- ⚡ Fast performance using caching

---

## 🛠 Tech Stack

- **Python**
- **Streamlit** – UI
- **LangChain** – LLM pipeline
- **FAISS** – Vector database
- **Sentence Transformers** – Embeddings
- **Ollama (TinyLlama / Phi-3)** – Local LLM

---

## ⚙️ How to Run Locally

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/llm-doc-assistant.git

# Go to project folder
cd llm-doc-assistant

# Create virtual environment
python -m venv venv

# Activate environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py