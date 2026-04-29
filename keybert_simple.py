import streamlit as st
import PyPDF2
from keybert import KeyBERT
import time

@st.cache_resource
def load_model():
    return KeyBERT()

kw_model = load_model()

st.title("Keyword Extractor using KeyBert")
st.write("Upload your document")

uploaded_file = st.file_uploader("Choose PDF", type=["pdf"])

if uploaded_file is not None:
    
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    
    if text:
        st.subheader("Extracted Keywords from KeyBert:")
        
        
        start_time = time.perf_counter()
        
        keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 1), stop_words='english', top_n=10)
        
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        
       
        st.info(f"Execution Time: {execution_time:.4f} seconds")
        
        for kw in keywords:
            st.success(f"Keyword: **{kw[0]}** (Accuracy: {round(kw[1], 2)})")
    else:
        st.error("The document cannot be read. Please try another one.")