import streamlit as st
from src.prompt import map_reduce_cheatsheet
from src.download import render_buttons
from src.rag_utils import retrieve_context
from src.user_promts import cheatsheet_prompt

text = st.session_state.get("pdf_notes")
if not text:
    st.switch_page("Home.py")


# Title
st.title("🧾Cheatsheet Generator")

# Output 

response = ""
with st.container(border=True):
    with st.spinner("🧠Generating Cheatsheet ......"):
            response = map_reduce_cheatsheet(text)
    st.markdown(response)
render_buttons(response)