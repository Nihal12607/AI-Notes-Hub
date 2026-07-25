import streamlit as st
from src.prompt import pt
from src.download import render_buttons
from src.rag_utils import retrieve_context
from src.ui import questionnaire_css
from src.user_promts import questionnaire_prompt

# CSS
questionnaire_css()

text = st.session_state.get("pdf_notes")

if not text:
    st.switch_page("Home.py")

# Title
st.title("📋 Questionnaire")
st.markdown("<br>",unsafe_allow_html=True)

# User Input
prompt = st.text_input("Prompt",placeholder="From Which Topics Would You Like To Generate Question ?(press enter)",label_visibility="collapsed")
st.markdown("<br>",unsafe_allow_html=True)

st.subheader("Choose Question Type :")
option = st.selectbox(
    "Question Type",
    ["MCQ's", "Descriptive Questions", "Mixed"],
    label_visibility="collapsed"
)
st.markdown("<br>",unsafe_allow_html=True)

st.subheader('Choose Difficulty : ')
diff = st.radio(
    "Difficulty",
    ["Easy","Medium","Hard"]
)

st.subheader("Number Of Questions :")
num = st.number_input("Number of questions",label_visibility="collapsed",step=1,value=10)
st.markdown("<br>",unsafe_allow_html=True)

generate = st.button("Generate")

response = ""
if generate:
    with st.container(border=True):
        with st.spinner("🧠 Generating Questions ...."):
            context = retrieve_context(prompt,top_k=6)
            context_to_send = context if context.strip() else text
            response = pt(questionnaire_prompt(prompt,context_to_send,option,diff,num))
        st.markdown(response)
    render_buttons(response)

