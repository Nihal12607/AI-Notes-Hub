import streamlit as st

def home_css():
    st.markdown("""
        <style>
            .block-container{
                padding-top:6rem;
            }
            .stButton button{
                background-color:#4F8BF9;
                margin-left:50px;
                color:white;
                width:150px;
                height:80px;
                border-radius:24px;
                font-size:22px;
                font-weight:800;

            }
            /* Hover */
            .stButton > button:hover{
                background-color:#3674e8;
                color:white;
            }

            /* Disabled button */
            .stButton > button:disabled {
                background-color: #2E3440;
                color: #8A8A8A;
                border: 1px solid #444;
                cursor: not-allowed;
            }
        </style>
        """,unsafe_allow_html=True)

def questionnaire_css():
    st.markdown("""
        <style>
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

