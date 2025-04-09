import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables from .env
load_dotenv()

# Fetch API key from environment
api_key = os.getenv("GEMINI_API_KEY")

# Check if the key is loading correctly
if not api_key:
    st.error("API key not found. Please check your .env file.")
    st.stop()

genai.configure(api_key=api_key)

# Initialize model
model = genai.GenerativeModel("gemini-2.0-flash")

def get_response(prompt):
    res = model.generate_content(prompt)
    return res.text

# Streamlit UI
st.set_page_config(page_title="🚀 Get set Go", layout="centered")
st.title("👽 WELCOME TO MY WORLD!!")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_area(
        label="prompt",
        key="input",
        placeholder="Ask Me Anything...",
        height=80,
        label_visibility="collapsed"
    )
    submit = st.form_submit_button("Send")

if submit and user_input.strip():
    st.session_state.messages.append({'role': 'user', 'text': user_input})
    try:
        bot_res = get_response(user_input)
        st.session_state.messages.append({'role': 'bot', 'text': bot_res})
    except Exception as e:
        st.error(f"Error: {e}")
    st.rerun()

with st.container(border=True, height=400):
    for message in st.session_state.messages:
        if message['role'] == 'user':
            st.markdown(
                f"<div style='color:#000000; background-color:#ffffff; padding:5px;margin: 5px 0; display: inline-block; max-width: 80%;border-radius:10px'>👤{message['text']}</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div style='color:#ffffff; background-color:#000000; padding:5px;margin: 5px 0; display: inline-block; max-width: 80%;border-radius:10px'>🤖{message['text']}</div>",
                unsafe_allow_html=True
            )
            st.divider()


