
import streamlit as st
from google import genai

st.title("🤖 My Chatbot")

# New Chat button
if st.button("🆕 New Chat"):
    st.session_state.messages = []
    st.rerun()

# Get API key
API_KEY = st.secrets["GEMINI_API_KEY"]

# Gemini client
client = genai.Client(api_key=API_KEY)

# Store conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
user_message = st.chat_input("Type your message...")

if user_message:

    # Show user message
    with st.chat_message("user"):
        st.write(user_message)

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    # Create conversation text
    conversation = ""

    for message in st.session_state.messages:
        conversation += message["role"] + ": "
        conversation += message["content"] + "\n"

    # Ask Gemini
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=conversation
    )

    answer = response.text

    # Show Gemini response
    with st.chat_message("assistant"):
        st.write(answer)

    # Save Gemini response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
