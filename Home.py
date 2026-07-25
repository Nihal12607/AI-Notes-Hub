import streamlit as st
from src.pdf_extracter import extract_pdf,extract_text
from src.rag_utils import index_document,load_embedder
from src.ui import home_css
import hashlib

# Page Info
st.set_page_config(
    page_title="AI Notes Hub",
    page_icon="📚",
    layout="wide"
)

# CSS
home_css()

# Title
st.title("📖 AI Notes Hub",text_alignment="center")
st.markdown("<br>", unsafe_allow_html=True)

# User Input
st.subheader("📂 Please Upload Your Notes")
st.markdown("<br>", unsafe_allow_html=True)

uploaded_file = st.file_uploader(label="Select file",
    type=["pdf","txt"],
    label_visibility="collapsed"
)
st.markdown("<br>", unsafe_allow_html=True)

# Text Extraction
text = " "
if uploaded_file:
    file_bytes = uploaded_file.read()
    file_hash = hashlib.sha256(file_bytes).hexdigest()

    if st.session_state.get("pdf_hash") != file_hash:    
        st.session_state["pdf_name"] = uploaded_file.name
        st.session_state["pdf_hash"] = file_hash
        extension = uploaded_file.name.split(".")[-1].lower()

        try:
            if extension == "pdf":
                text = extract_pdf(file_bytes)
            elif extension == "txt":
                text = extract_text(file_bytes)

            if not text or not text.strip():
                st.error("❌ No readable text was found in the uploaded file, Try Again")
                st.session_state.pop("pdf_notes", None)
            else:
                st.session_state["pdf_notes"] = text
                # CRITICAL: Call index_document here to populate ChromaDB!
                with st.spinner("⚡Analyzing document ...."):
                    index_document(text)

        except Exception as e:
            st.error("❌ Failed to read the file, Try Again")
            st.session_state.pop("pdf_notes", None)

if "pdf_notes" in st.session_state:
    st.success(f"{st.session_state["pdf_name"]}  has been  Uploaded")

st.markdown("<br><br>", unsafe_allow_html=True)

# Buttons

col1,col2,col3,col4 = st.columns(4)

with col1:
    summarize = st.button("Summarize", disabled=(st.session_state.get("pdf_notes") is None))
with col2:
    explainer = st.button("Explain Concepts",disabled=(st.session_state.get("pdf_notes") is None))
with col3:
    questionnaire = st.button("Generate Questions", disabled=(st.session_state.get("pdf_notes") is None))
with col4:
    cheatsheet = st.button("Generate CheatSheets",disabled=(st.session_state.get("pdf_notes") is None))

if summarize:
    st.switch_page("pages/1_Summarizer.py")

if explainer:
    st.switch_page("pages/2_Explainer.py")

if questionnaire:
    st.switch_page("pages/3_Questionnaire.py")

if cheatsheet:
    st.switch_page("pages/4_Cheatsheet.py")