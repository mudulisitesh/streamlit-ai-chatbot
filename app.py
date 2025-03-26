import streamlit as st
import google.generativeai as genai
import os

# Streamlit page config
st.set_page_config(page_title="Gemini AI Chatbot", page_icon="💬", layout="wide")

# Custom CSS for a better chat UI
st.markdown(
    """
    <style>
        body {
            background-color: #121212;
            color: white;
        }
        .main {
            background-color: #1E1E1E;
            padding: 20px;
            border-radius: 10px;
        }
        .chat-container {
            max-width: 800px;
            margin: auto;
        }
        .user-message {
            background-color: #0078FF;
            color: white;
            padding: 12px;
            border-radius: 12px;
            margin: 8px;
            max-width: 75%;
            align-self: flex-end;
        }
        .bot-message {
            background-color: #2E2E2E;
            color: white;
            padding: 12px;
            border-radius: 12px;
            margin: 8px;
            max-width: 75%;
            align-self: flex-start;
        }
        .message-container {
            display: flex;
            flex-direction: column;
        }
        .input-container {
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 10px;
            position: fixed;
            bottom: 10px;
            width: 80%;
            max-width: 800px;
            left: 50%;
            transform: translateX(-50%);
            background-color: #1E1E1E;
            border-radius: 10px;
            box-shadow: 0px 0px 8px rgba(255, 255, 255, 0.1);
        }
        .input-container input {
            width: 100%;
            padding: 10px;
            border-radius: 8px;
            border: none;
            outline: none;
            font-size: 16px;
        }
        .send-btn {
            background-color: #0078FF;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 8px;
            cursor: pointer;
            margin-left: 10px;
            transition: 0.3s;
        }
        .send-btn:hover {
            background-color: #005BBB;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar for API Key input
st.sidebar.title("🔑 API Key")
api_key = st.sidebar.text_input("Enter your Google Gemini API Key:", type="password")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Chat interface
st.title("💬 Gemini AI Chatbot")
st.markdown("A sleek AI chatbot powered by Google Gemini.")

# Chat display
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for message in st.session_state["messages"]:
    role, text = message
    css_class = "user-message" if role == "user" else "bot-message"
    st.markdown(f'<div class="message-container"><div class="{css_class}">{text}</div></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Input field for user message
st.markdown('<div class="input-container">', unsafe_allow_html=True)
user_input = st.text_input("Type your message here:", key="user_input", label_visibility="collapsed")
if st.button("Send", key="send-btn"):
    if not api_key:
        st.warning("Please enter your Google Gemini API key in the sidebar.")
    elif user_input:
        try:
            # Configure Gemini API
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.0-flash")

            # Call Gemini API
            response = model.generate_content(user_input)
            bot_reply = response.text

            # Update chat history
            st.session_state["messages"].append(("user", user_input))
            st.session_state["messages"].append(("bot", bot_reply))

            # Refresh page
            st.rerun()
        except Exception as e:
            st.error(f"Error: {str(e)}")
st.markdown('</div>', unsafe_allow_html=True)
