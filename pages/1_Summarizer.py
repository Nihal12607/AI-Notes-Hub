import streamlit as st
from src.prompt import pt
from src.download import render_buttons
from src.rag_utils import retrieve_context
from src.user_promts import summarize_prompt

text = st.session_state.get("pdf_notes")
if not text:
    st.switch_page("Home.py")


# Title
st.title("🧾AI Summarizer")

# Prompt
prompt = st.text_input("Prompt",placeholder="What would you like to Summarize ? (press enter to generate)",label_visibility="collapsed")

# Output 


response = ""
if bool(prompt.strip()):
    with st.container(border=True):
        with st.spinner("🧠 Generating Summary ......"):

            context = retrieve_context(prompt,top_k=2)
            context_to_send = context if context.strip() else text
            response = pt(summarize_prompt(prompt,context_to_send))
            
        st.markdown(response)
    render_buttons(response)
    