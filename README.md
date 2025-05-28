# 📚 Student Handbook Assistant

An AI-powered assistant built with Streamlit and Gemini API that allows students to query their university handbook in natural language. This tool simplifies navigation through dense PDF documents, making it easy to find policies on grading, attendance, discipline, and more.

## 🚀 Features

- 🔍 Ask natural language questions about the handbook
- 🤖 Powered by Google Gemini AI (Gemini 2.0 Flash)
- 📄 Handles PDF parsing using PyMuPDF
- 🧠 Uses keyword relevance to extract and rank relevant content
- 🧰 Integrated with LangChain's vector store and HuggingFace embeddings (scalable design)
- 📥 Downloadable handbook viewer

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **AI Model**: Google Gemini (via `google.generativeai`)
- **Document Handling**: PyMuPDF, LangChain
- **Environment**: Python 3.10+
- **Embeddings**: HuggingFaceEmbeddings (planned for vector search)
- **Storage**: FAISS (planned for enhanced semantic retrieval)

## 🧠 How It Works
1. The user selects a handbook PDF.

2. The content is extracted and split into paragraphs.

3. The user asks a question in plain English.

4. Relevant paragraphs are ranked using keyword overlap.

5. The top context is sent to Gemini with the question for a natural-language response.

## 📦 Setup Instructions

1. **Install dependencies**
    ```bash
      pip install -r requirements.txt
      Add your Gemini API key
2. **Create a .env file in the root directory:**
     ```ini
        GEMINIAI_API_KEY=your_gemini_api_key
3. **Add your handbook PDF**
Place your handbook.pdf in the project root or update the path in the code.

4. **Run the app**


## 👨‍💻 Author
Baldo G. Otu-Quayson

 ```bash
    streamlit run Student_assistant.py
