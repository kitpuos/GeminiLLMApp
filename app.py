from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
import google.generativeai as genai

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

## Function to load a Gemini model and get responses

model_name = "gemini-1.5-flash"

def get_gemini_response(prompt):
    """Load a Gemini model and get a response for the given prompt."""
    model = genai.GenerativeModel(model_name = model_name)
    response = model.generate_content(prompt)
    return response.text

## Streamlit app setup

st.set_page_config(page_title="Gemini Model Demo", page_icon=":robot_face:")
st.title("Gemini Model Demo")
st.header("Generate Content with Gemini")

input = st.text_input("Enter your prompt: ", key = "input")
submit_button = st.button("Generate")

## WHen the button is clicked, get the response from the Gemini model
if submit_button:
    if input:
        with st.spinner("Generating response..."):
            response = get_gemini_response(input)
            st.success("Response generated successfully!")
            st.subheader("Response:")
            st.write(response)
    else:
        st.error("Please enter a prompt before clicking the button.")
else:
    st.warning("Please click the button to generate a response.")