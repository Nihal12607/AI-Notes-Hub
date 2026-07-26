import streamlit as st
from src.pdf_extracter import extract_pdf,extract_text
from src.rag_utils import index_document,load_embedder
from src.ui import home_css
from src.rag_utils import retrieve_context
import hashlib

# Page Info
st.set_page_config(
    page_title="AI Notes Hub",
    page_icon="📚",
    layout="wide",
)

# CSS
home_css()

# Title
st.title("📖 AI Notes Hub",text_alignment="center")
st.markdown("<br>", unsafe_allow_html=True)

# User Input
st.subheader("📂 Please Upload Your Notes")
st.markdown("<br>", unsafe_allow_html=True)

uploaded_files = st.file_uploader(label="Select file",
    type=["pdf","txt"],
    label_visibility="collapsed",
    accept_multiple_files=True
)
st.markdown("<br>", unsafe_allow_html=True)

# Text Extraction
if uploaded_files and len(uploaded_files)<5:

    # Create a hash for the entire upload
    hash_object = hashlib.sha256()

    for file in uploaded_files:
        hash_object.update(file.read())
        file.seek(0)

    upload_hash = hash_object.hexdigest()

    if st.session_state.get("upload_hash") != upload_hash:

        st.session_state["upload_hash"] = upload_hash

        combined_text = ""
        uploaded_names = []

        with st.spinner("⚡ Extracting documents ....."):

            for uploaded_file in uploaded_files:

                file_bytes = uploaded_file.read()
                extension = uploaded_file.name.split(".")[-1].lower()

                try:

                    if extension == "pdf":
                        text = extract_pdf(file_bytes)

                    elif extension == "txt":
                        text = extract_text(file_bytes)

                    else:
                        continue

                    if not text or not text.strip():
                        st.warning(f"⚠️ {uploaded_file.name} contains no readable text.")
                        continue

                    # Store filename
                    uploaded_names.append(uploaded_file.name)

                    # Add separator between files
                    combined_text += (
                        f"\n\n==============================\n"
                        f"FILE: {uploaded_file.name}\n"
                        f"==============================\n\n"
                    )

                    combined_text += text

                except Exception:
                    st.warning(f"❌ Failed to read {uploaded_file.name}")
       
            index_document(combined_text)
            

        if combined_text.strip():
            st.session_state["pdf_notes"] = combined_text
            st.session_state["pdf_names"] = uploaded_names
        else:
            st.session_state.pop("pdf_notes", None)
            st.session_state.pop("pdf_names", None)

elif uploaded_files :
    st.error("❌ You can upload a maximum of 5 files.")

# Success Message
if "pdf_notes" in st.session_state:

    st.success("✅ Files uploaded successfully!")

    for name in st.session_state["pdf_names"]:
        st.write(f"📄 {name}")


# Buttons
st.markdown("<br>",unsafe_allow_html=True)
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