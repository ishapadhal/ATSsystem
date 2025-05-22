from dotenv import load_dotenv

load_dotenv()
import base64
import streamlit as st
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
def get_gemini_responce(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## convert pdf to image
        images=pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]

        #convert to bytes
        img_byte_arr= io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr=img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type":"image/jpeg",
                "data":base64.b64encode(img_byte_arr).decode()
            }
        
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("no file uploaded")
    
##
st.set_page_config(page_title="ATs resume expert")
st.header("ATS tracking system")
job_description=st.text_area("job Description :" , key="input")
uploaded_file=st.file_uploader("uploaded your resume(PDF)...",type=["pdf"])

if uploaded_file is not None:
    st.write("PDF uploaded successfully")


submit1= st.button("Tell me about resume")

#submit2= st.button("How can i improvise my skill")

submit2= st.button("percentage match")

if submit1:
    if uploaded_file is not None:
        pdf_Content=input_pdf_setup(uploaded_file)
        responce= get_gemini_responce(input_prompt1,pdf_Content,job_description)
        st.subheader("The Responce is ")
        st.write(responce)
    else:
        st.write("please upload the resume")
        
elif submit2:
    if uploaded_file is not None:
        pdf_Content=input_pdf_setup(uploaded_file)
        responce= get_gemini_responce(input_prompt2,pdf_Content,job_description)
        st.subheader("The Responce is ")
        st.write(responce)
    else:
        st.write("please upload the resume")