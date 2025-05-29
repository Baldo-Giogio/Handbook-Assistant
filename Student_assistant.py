import os
from dotenv import load_dotenv
import streamlit as st
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import PyMuPDFLoader
import google.generativeai as genai
import re
import base64

st.title("Student Handbook Assistant")
st.subheader(" 📚Academic City Handbook Assistant")
st.write("This section uses a large language model to help users explore and understand the school's handbook. You can ask questions in natural language—like policies on attendance, grading, or discipline—and get clear, accurate answers pulled directly from the official document.")
st.write("It is a smart, searchable guide designed to make the handbook easier and faster to navigate.")

load_dotenv()
api_key = os.getenv("GEMINIAI_API_KEY")
genai.configure(api_key=api_key)
llm = genai.GenerativeModel("gemini-2.0-flash")


st.markdown("Ask anything you would like to know")


def read_text(data_path):
    try:
        with open(data_path, "rb") as file:
            reader = PyMuPDFLoader(data_path)
            docs = reader.load()

            return "\n".join([doc.page_content for doc in docs])
    except Exception as e:
        st.error(f"Error loading Handbook: {str(e)}")
        return ""
        
def get_pdf_base64(data_path):
    try:
        with open(data_path, "rb") as f:
            return base64.b64encode(f.read()).decode('utf-8')
    except Exception as e:
        st.error(f"Error encoding PDF: {e}")
        return ""    

            
def pdf_download(data_path):

    if st.button("Download PDF"):
        base64_pdf = get_pdf_base64(data_path)
        file = os.path.basename(data_path)
        st.session_state.pdf_ready = True
        st.session_state.base64_pdf = base64_pdf
        st.session_state.file_name = file
        st.rerun()
if 'pdf_ready' in st.session_state and st.session_state.pdf_ready:
    if st.download_button("Download PDF", data=st.session_state.base64_pdf, 
                        file_name=st.session_state.file_name, mime="application/pdf"):
        st.info("Download the PDF and view it with your local PDF reader or browser.")
        st.session_state.pdf_ready = False


data_source={"Academic City Student Handbook (PDF)": "handbook.pdf"}

data_set = st.selectbox("Load Handbook", list(data_source))
select_path = data_source[data_set]
content = ""

if select_path.endswith (".pdf"):

    with st.spinner("Processing PDF..."):
        content = read_text(select_path)
        
    with st.expander("Download Options"):
                pdf_download(select_path)
else: 
    st.error("Unsupported File Format")

paragraphs = content.split("\n\n")
num_pages = 5
question= st.text_input("What would you like to know from the Handbook? ")

if question:
    question_con = set(re.findall(r'\w+', question.lower()))
    rank = []

    for par in paragraphs:
        p_con = set(re.findall(r'\w+', par.lower()))
        score = len(question_con.intersection(p_con))
        rank.append((score, par))
    rank.sort(key = lambda x: x[0], reverse = True)

    max_pages = min(num_pages, len(rank))
    retrieve_context = "\n\n".join([par for score, par in rank[:max_pages]])

else:
    retrieve_context = content

if st.button("Ask Handbook Assistant"):
    if retrieve_context and question:
        with st.spinner("Retreiving Response"):
            try:
                prompt = f"From the handbook: \n{retrieve_context}\n\nYou asked {question}\n\n According to the handbook:"

                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)
                st.success("Here You Go:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Response not found: {str(e)}")
                st.write("Question is not in the handbook. Please try again")
    else:
        st.warning("Please ask a question")
