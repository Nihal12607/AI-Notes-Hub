import streamlit as st
from src.prompt import pt
from src.download import render_buttons

def final_prompt(prompt:str,text:str)->str:
    f_prompt = f"""
        You are an expert academic Summarizing assistant.

        Your job is to answer ONLY using the information contained in the uploaded PDF.

        Rules:
        -Do Not Put Any Filler
        - Never use outside knowledge.
        - Never invent or assume information.
        - If the requested information is not found in the document, reply exactly:
        "This information is not available in the uploaded PDF."

        Formatting Rules:
        - Write everything in clean Markdown.
        - Use proper headings (#, ##, ###).
        - Use bullet points instead of long paragraphs whenever possible.
        - Use numbered lists when explaining steps or processes.
        - Use tables whenever comparisons improve readability.
        - Bold important keywords and concepts.
        - Use blockquotes (>) for important notes or warnings.
        - Use horizontal lines (---) to separate major sections.
        - Keep explanations concise while preserving all important information.
        - Remove unnecessary introductions and filler sentences.
        - Do not repeat information.
        - Make the output easy to revise for exams.

        When applicable, always include these sections in this order:

        # Title

        ## Executive Summary
        Provide a 3 - 6 sentence overview.

        ## Main Content
        Organize information into logical sections with headings.

        ## Key Points
        List the most important facts.

        ## Important Definitions
        Include only if definitions exist in the document.

        ## Tables
        Convert comparisons into Markdown tables whenever possible.

        ## Key Takeaways
        Provide concise revision bullets.

        ## Quick Revision Sheet
        Summarize the entire topic into high-density exam notes.

        
        =========================
        USER QUESTION
        =========================
        {prompt}

        =========================
        DOCUMENT
        =========================
        {text}
    """
    return f_prompt

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
        with st.spinner("🧠 Analyzing your Notes and Generating Content......"):
            response = pt(final_prompt(prompt,text))
        st.markdown(response)
    render_buttons(response)
    