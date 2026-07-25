import streamlit as st

def render_buttons(response:str) -> None:
    if not response:
        return
    st.markdown("<br>",unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    base_name = st.session_state.get("pdf_name", "notes").rsplit(".", 1)[0]

    with col1:
        st.download_button(
            label="📄 Download as Markdown (.md)",
            data=response,
            file_name=f"{base_name}_notes.md",
            mime="text/markdown",
            use_container_width=True,
        )

    with col2:
        st.download_button(
            label="📝 Download as Plain Text (.txt)",
            data=response,
            file_name=f"{base_name}_notes.txt",
            mime="text/plain",
            use_container_width=True,
        )