import os
from dotenv import load_dotenv
import streamlit as st
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import PyMuPDFLoader
import google.generativeai as genai
import re


def LLM():
    st.title("Student Handbook Assistant")
    st.subheader(" 📚Academic City Handbook Assistant")
    st.write("This section uses a large language model to help users explore and understand the school's handbook. You can ask questions in natural language—like policies on attendance, grading, or discipline—and get clear, accurate answers pulled directly from the official document.")
    st.write("It is a smart, searchable guide designed to make the handbook easier and faster to navigate.")

    load_dotenv()
    api_key = os.getenv("GEMINIAI_API_KEY")
    genai.configure(api_key=api_key)
    llm = genai.GenerativeModel("gemini-2.0-flash")


    st.markdown("Ask anything you would like to know")


    def read_text(data_source):
        try:
            with open(data_source, "rb") as file:
                reader = PyMuPDFLoader
                docs = reader.load()

                return "\n".join([docs.extract_text() or "" for docs in reader.docs])
        except Exception as e:
            st.error("Error loading Handbook")
            return ""
        
    def get_pdf_base64(data_source):
        try:
            import base64
            with open(data_source, "rb") as f:
                return base64.b64encode(f.read()).decode('utf-8')
        except Exception as e:
            st.error(f"Error encoding PDF: {e}")
            return ""    
        
    def pdf_download(data_source):
            base64_pdf = get_pdf_base64(data_source)
            file_name = os.path.basename(data_source)
            st.download_button("Download PDF", data=base64_pdf, file_name=file_name, mime="application/pdf")
            st.info("Download the PDF and view it with your local PDF reader or browser.")
    
    
    data_source={
       "Academic City Student Handbook (PDF)": "handbook.pdf"
    }

    data_set = st.selectbox("Load Handbook", list(data_source))
    select_path = data_source[data_set]
    content = ""

    st.subheader("PDF Preview")
    if select_path.endswith (".pdf"):
        with st.spinner("Processing PDF..."):
            pdf_download(select_path)
            content = read_text(select_path)
    else: 
        st.error("Unsupported File Format")

    paragraphs = content.split("\n\n")
    question= st.text_input("What would you like to know about the Handbook? ")

    if question:
        question_con = set(re.findall(r'\w+', question.lower))
        rank = []

        for par in paragraphs:
            p_con = set(re.findall(r'\w+', p_con.lower()))
            score = len(question_con.intersection(p_con))
            rank.append((score, p_con))
        rank.sort(key = lambda x: x[0], reverse = True)

        retrieve_context = "\n\n".join([p_con for score, p_con in rank[paragraphs]])

    else:
        retrieve_context = content

    st.write("Ask Your Question")
    if st.button("Ask Handbook Assistant"):
        if retrieve_context and question:
            with st.spinner("Retreiving Response"):
                try:
                    response = genai.generate_content([retrieve_context, question])
                    st.success("Here You Go:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Response not found")
        else:
            st.warning("Please ask a question")