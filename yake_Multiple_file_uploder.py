import streamlit as st
import PyPDF2
import yake

def extract_keywords_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    full_text = ""
    for page in pdf_reader.pages:
        content = page.extract_text()
        if content:
            full_text += content

    if not full_text.strip():
        return None

    kw_extractor = yake.KeywordExtractor(lan="en", n=2, dedupLim=0.9, top=100, features=None)
    keywords = kw_extractor.extract_keywords(full_text)
    return keywords

st.set_page_config(page_title="YAKE! Keyword Extractor")
st.title("PDF Keyword Extractor (YAKE!)")


uploaded_files = st.file_uploader("Upload your PDF files", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        st.write(f"---")
        st.subheader(f"File: {uploaded_file.name}")
        
        with st.spinner(f'Extracting keywords from {uploaded_file.name}...'):
            results = extract_keywords_from_pdf(uploaded_file)
            
            if results:
                st.write("Note: Lower score means higher relevance in YAKE!")
                
                for kw, score in results:
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.info(f"**{kw}**")
                    with col2:
                        st.write(f"Score: `{round(score, 4)}`")
            else:
                st.error(f"Could not extract text from {uploaded_file.name}. Please check the file.")