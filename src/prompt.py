from google import genai
from google.genai import types
import os
import streamlit as st

@st.cache_resource(show_spinner=False)
def get_gemini_client() -> genai.Client | None:
    
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        st.error("🔑 GEMINI_API_KEY environment variable is missing!")
        return None

    # This client initialization happens only on a cache miss
    return genai.Client(api_key=api_key)

def pt(f_prompt:str) -> str:
    client = get_gemini_client()

    response = client.models.generate_content(
        model='gemini-3.1-flash-lite',
        contents=f_prompt,
        config=types.GenerateContentConfig(
            temperature = 0.005, 
        )
    )

    return response.text