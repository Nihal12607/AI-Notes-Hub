from google import genai
from google.genai import types
import os
import streamlit as st
import time

@st.cache_resource(show_spinner=False)
def get_gemini_client() -> genai.Client | None:
    
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        st.error("🔑 GEMINI_API_KEY environment variable is missing!")
        return None

    # This client initialization happens only on a cache miss
    return genai.Client(api_key=api_key)

def pt(f_prompt: str) -> str:
    client = get_gemini_client()
    if not client:
        return "API Client not available."

    # Priority list of models to try in order
    MODELS_TO_TRY = [
        'gemini-3.1-flash-lite',
        'gemini-3.5-flash',
        'gemini-3.5-flash-lite',
        'gemini-2.5-flash-lite',
        'gemini-2.5'
    ]

    for model_name in MODELS_TO_TRY:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=f_prompt,
                config=types.GenerateContentConfig(
                    temperature=0.005,
                )
            )
            # If successful, return the text immediately
            return response.text

        except ServerError as e:
            # Catches 503 / 500 server errors specifically
            st.warning(f"⚠️ {model_name} is currently busy (503). Retrying with alternative model...")
            time.sleep(1)  # Brief wait before failing over
            continue

        except APIError as e:
            # Handles rate limits or other API errors
            st.warning(f"⚠️ Failed on {model_name}: {e}. Retrying with next model...")
            time.sleep(1)
            continue

        except Exception as e:
            st.error(f"Unexpected error: {e}")
            break

    return "❌ All available Gemini models failed or are currently unavailable. Please try again shortly."


def map_reduce_cheatsheet(text: str, chunk_size: int = 100_000) -> str:
    # 1. Split text into manageable chunks
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    
    sub_summaries = []
    
    # 2. MAP: Generate mini cheatsheets for each chunk
    for idx, chunk in enumerate(chunks):
        prompt = f"Create a concise technical cheatsheet summary for this section of notes:\n\n{chunk}"
        
        # Small sleep to stay safe under per-minute rate limits
        time.sleep(2) 
        
        sub_summary = pt(prompt)
        sub_summaries.append(sub_summary)
    
    # 3. REDUCE: Combine all mini cheatsheets into one master cheatsheet
    combined_notes = "\n\n--- SECTION BREAK ---\n\n".join(sub_summaries)
    final_prompt = f"Combine the following section summaries into one cohesive, beautifully organized master cheatsheet:\n\n{combined_notes}"
    
    return pt(final_prompt)