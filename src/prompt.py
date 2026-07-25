from google import genai
from google.genai import types
import os
import streamlit as st

def pt(f_prompt:str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("🔑 API Key missing! Please set GEMINI_API_KEY in your environment.")
        return ""

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model='gemini-3.1-flash-lite',
        contents=f_prompt,
        config=types.GenerateContentConfig(
            temperature = 0.005, 
        )
    )

    return response.text