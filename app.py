from google import genai
from google.genai import types
from PIL import Image
import streamlit as st
import io
import os
from dotenv import load_dotenv


load_dotenv()


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.title("Chat with Neko the Cat 🐱")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

uploaded_image = st.file_uploader("Upload an image (optional)", type=['png', 'jpg', 'jpeg'])

message = st.chat_input("Your Message")

def generate_response(message, image=None):
    contents = [message]

    if image:
        pil_image = Image.open(image)
        contents = [pil_image, message]

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction="You are a cat. Your name is Neko. Respond in a cute, cat-like manner."
        ),
        contents=contents
    )

    return response

if message:
    st.session_state.messages.append({"role": "user", "content": message})

    with st.chat_message("user"):
        st.write(message)

    with st.chat_message("assistant"):
        with st.spinner("Neko is thinking... 🐱"):
            response = generate_response(message, uploaded_image)

            if response:
                st.write(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
 