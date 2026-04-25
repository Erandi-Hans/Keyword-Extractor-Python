import streamlit as st
import PyPDF2
import yake

def extract_keywords_from_pdf(pdf_file):
    # 1. Read PDF content
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    full_text = ""
    for page in pdf_reader.pages:
        content = page.extract_text()
        if content:
            full_text += content

    if not full_text.strip():
        return None

    # 2. Configure YAKE!
    # n = max words in a phrase (1 for single words)
    # top = number of keywords to extract
    kw_extractor = yake.KeywordExtractor(lan="en", n=1, dedupLim=0.9, top=10, features=None)
    
    # 3. Extract keywords
    keywords = kw_extractor.extract_keywords(full_text)
    return keywords

# Streamlit UI
st.set_page_config(page_title="YAKE! Keyword Extractor")
st.title("PDF Keyword Extractor (YAKE!)")

uploaded_file = st.file_uploader("Upload your 2-page PDF", type=["pdf"])

if uploaded_file is not None:
    with st.spinner('Extracting keywords...'):
        results = extract_keywords_from_pdf(uploaded_file)
        
        if results:
            st.subheader("Top Extracted Keywords:")
            st.write("Note: Lower score means higher relevance in YAKE!")
            
            for kw, score in results:
                # Using columns to display keyword and score neatly
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.info(f"**{kw}**")
                with col2:
                    st.write(f"Score: `{round(score, 4)}`")
        else:
            st.error("Could not extract text from this PDF. Please check the file.")