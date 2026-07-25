import streamlit as st
from src.prompt import pt
from src.download import render_buttons
from src.rag_utils import retrieve_context
from src.user_promts import explain_prompt


text = st.session_state.get("pdf_notes")
if not text:
    st.switch_page("Home.py")


# Title
st.title("🧾 Explain Concepts")

# Prompt
prompt = st.text_input("Prompt",placeholder="What would you like to Learn ?  (press enter to generate)",label_visibility="collapsed")

# Output 


response = ""
if bool(prompt.strip()):
    with st.container(border=True):
        with st.spinner("🧠 Generating Explanation ......"):            
            context = retrieve_context(prompt,top_k=6)
            context_to_send = context if context.strip() else text
            response = pt(explain_prompt(prompt,context_to_send))

        st.markdown(response)
    render_buttons(response)