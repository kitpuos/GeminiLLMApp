from dotenv import load_dotenv
load_dotenv()

import os
import math
import streamlit as st
import google.generativeai as genai
from PIL import Image

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

## Function to load a Gemini model and get responses

model_name = "gemini-1.5-flash"

def get_gemini_response(image, prompt):
    """Load a Gemini model and get a response for a given image with/without a prompt."""
    model = genai.GenerativeModel(model_name = model_name)

    ## Create the content list with the image and optional prompt
    content = list(images)

    if prompt:
        content.append(prompt)
    
    if not content:
        st.error("Please upload at least one image or provide a prompt.")
        return ""
    
    response = model.generate_content(content)
    return response.text

## Streamlit app setup

st.set_page_config(page_title="Gemini Vision Demo", page_icon=":robot_face:")
st.title("🤖 Gemini Vision Demo")
st.header("Generate Content from Images + Text Prompt")

uploaded_images = st.file_uploader("Upload images", type=["jpg", "jpeg", "png"], key="images", accept_multiple_files=True)

images = []

if uploaded_images:
    # Open images with PIL and resize thumbnails
    thumbnail_size = (1080, 1080)
    resized_images = []
    for file in uploaded_images:
        img = Image.open(file)
        img_copy = img.copy()
        img_copy.thumbnail(thumbnail_size)
        resized_images.append(img_copy)
        images.append(img)  # Keep original for model

    # Display uploaded images in a responsive grid
    num_images = len(resized_images)
    max_columns = 4
    num_columns = min(num_images, max_columns)
    rows = math.ceil(num_images / num_columns)

    st.subheader("Uploaded Image(s):")

    for row in range(rows):
        cols = st.columns(num_columns)
        for col in range(num_columns):
            idx = row * num_columns + col
            if idx < num_images:
                with cols[col]:
                    st.image(resized_images[idx], caption=f"Image {idx + 1}", use_container_width=True)

    st.markdown("You can provide an **optional prompt** below to guide the model.")

    prompt = st.text_input("Enter your prompt (optional):", key="prompt")

    # Submit button (enabled only if images are uploaded)
    submit_button = st.button("Generate", disabled=not images)

    if submit_button:
        with st.spinner("Generating response..."):
            response = get_gemini_response(images, prompt)
            if response:
                st.success("✅ Response generated successfully!")
                st.subheader("Response:")
                st.write(response)
else:
    st.warning("⚠️ Please upload at least one image to begin.")