import streamlit as st
from src.prompt import pt
from src.download import render_buttons

def final_prompt(topic: str,text: str,option: str,difficulty: str,num_questions: int) -> str:

    f_prompt = f"""
        You are an expert academic Question Generator.

        Your task is to generate questions ONLY from the uploaded document.

        ========================
        GENERAL RULES
        ========================

        - NEVER use outside knowledge.
        - NEVER invent information.
        - Generate questions ONLY from the uploaded document.
        - If the requested topic is not found, reply:
        "The requested topic is not available in the uploaded document."
        - Do not include introductions or conclusions.
        - Return Markdown only.
        - If the topic is empty, generate questions from the whole document.
        - Avoid asking questions from the Preface, Contents or Index.

        ========================
        USER REQUEST
        ========================

        Topic:
        {topic if topic.strip() else "Whole Document"}

        Question Type:
        {option}

        Difficulty:
        {difficulty}

        Number of Questions:
        {num_questions}

        ========================
        QUESTION TYPE RULES
        ========================

        If Question Type is "MCQ's":

        - Generate exactly {num_questions} MCQs.
        - One question per line.
        - Four options (A,B,C,D).
        - Display options in a 2x2 markdown table.
        - Keep options short.
        - Do NOT reveal the answers.
        - At the end, generate an Answer Key section.

        Example:

        1. What is a tuple?

        | A | B |
        |---|---|
        | Mutable | Immutable |
        | Dictionary | Set |

        --------------------------------------

        If Question Type is "Descriptive Questions":

        Generate exactly {num_questions} descriptive questions.

        Questions should include a mix of:
        - Short Answer
        - Long Answer
        - Explain
        - Compare
        - Define
        - List
        - Application-based questions

        At the end generate an Answer Key with concise model answers.

        --------------------------------------

        If Question Type is "Mixed":

        Determine the subject automatically.

        Programming Subjects:
        - 30% MCQs
        - 30% Coding Problems
        - 20% Debugging Questions
        - 20% Output Prediction

        For every MCQ inside Mixed Questions, use EXACTLY the same formatting rules as the MCQ section.

        Each MCQ must be formatted as:

        1. Question

        | A | B |
        |---|---|
        | Option A | Option B |
        | Option C | Option D |

        Leave one blank line before and after each table.

        Do not write Markdown tables on a single line.

        Mathematics:
        - MCQs
        - Numerical Problems
        - Proofs
        - Derivations

        Science:
        - MCQs
        - Numerical Problems
        - Theory

        Theory Subjects:
        - MCQs
        - Short Answer
        - Long Answer
        - Case Study

        At the end provide an Answer Key.

        ========================
        DIFFICULTY
        ========================

        Easy:
        - Direct questions
        - Basic concepts

        Medium:
        - Conceptual understanding
        - Moderate application

        Hard:
        - Analytical
        - Multi-concept
        - Exam level
        - Give Harder Options (Mcq's)
        ========================
        DOCUMENT
        ========================

        {text}
        """

    return f_prompt


# CSS
st.markdown("""
<style>
    .block-container{
        padding-top:9rem;
    }
    .stButton button{
        background-color:#4F8BF9;
        color:white;
        width:100px;
        height:40px;
        border-radius:24px;
        font-size:22px;
        font-weight:800;

    }
    /* Hover */
    .stButton > button:hover{
        background-color:#3674e8;
        color:white;
    }
</style>
""",unsafe_allow_html=True)

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
        with st.spinner("🧠 Generating Questions...."):
            response = pt(final_prompt(prompt,text,option,diff,num))
        st.markdown(response)
    render_buttons(response)

