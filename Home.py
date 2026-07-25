import streamlit as st
from src.pdf_extracter import *

# CSS
st.markdown("""
<style>
    .block-container{
        padding-top:9rem;
    }
    .stButton button{
        background-color:#4F8BF9;
        margin-left:50px;
        color:white;
        width:150px;
        height:80px;
        border-radius:24px;
        font-size:22px;
        font-weight:800;

    }
    /* Hover */
    .stButton > button:hover{
        background-color:#3674e8;
        color:white;
    }

    /* Disabled button */
    .stButton > button:disabled {
        background-color: #2E3440;
        color: #8A8A8A;
        border: 1px solid #444;
        cursor: not-allowed;
    }
</style>
""",unsafe_allow_html=True)


# Page Info
st.set_page_config(
    page_title="AI Notes Hub",
    page_icon="📚",
    layout="wide"
)

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
doc = " "
if uploaded_file:
    st.toast("📓file Uploaded")
    file_bytes = uploaded_file.read()
    st.session_state["pdf_name"] = uploaded_file.name

    extension = uploaded_file.name.split(".")[-1].lower()

    if extension == "pdf":
        text = extract_pdf(file_bytes)
        st.session_state["pdf_notes"] = text

    elif extension == "txt":
        text = extract_text(file_bytes)
        st.session_state["pdf_notes"] = text


if "pdf_notes" in st.session_state:
    st.success(f"{st.session_state["pdf_name"]}  has been  Uploaded")

st.markdown("<br>", unsafe_allow_html=True)

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