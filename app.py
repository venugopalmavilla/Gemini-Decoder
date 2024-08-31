### gemini decode
from dotenv import load_dotenv

load_dotenv() ## load all the environment variables
import streamlit as st
# initilize streamlit app
st.set_page_config(page_title="GeminiDecode: Multilanguage Document Extraction by Gemini Pro")
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

input_prompt="""
You are expert in understanding invoices.
We will upload a image as invoice and you will have to answer any questions based on the uploaded invoice image.
Remember the current location is Bengaluru, Karnataka, India.
"""

## Function to load Google Gemini Pro Vision API And get respone

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
    # Read the file into bytes
      bytes_data = uploaded_file.getvalue()
      image_parts = [
       {
          "mime_type": uploaded_file.type, # Get the mime type of the uploaded file
          "data": bytes_data
       }
      ]
      return image_parts
    else:
      raise FileNotFoundError("No file uploaded")
    

def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content([input, image[0], prompt])
    return response.text

#stream lit app design

st.header("GeminiDecode: Multilanguage Document Extraction by Gemini Pro")
text= "Utilizing Gemini Pro AI, this project effortlessly extracts vital information + \
from diverse multilingual documents, transcending language barriers with \nprecision and + \
efficiency for enhanced productivity and decision-making."

styled_text = f"<span style='font-family:serif;'>{text}</span>"
st.markdown(styled_text, unsafe_allow_html=True)

# input=st.text_input("Input Prompt:", key="input")
uploaded_file = st.file_uploader("Choose an image of the document:", type=["jpg", "jpeg", "png"])

image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

submit = st.button("Tell me about the document")

# If submit button is clicked
if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, image)

    st.subheader("The response is")
    st.write(response)