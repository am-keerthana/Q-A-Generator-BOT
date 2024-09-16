from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import PyPDF2
import openai
import os
from dotenv import load_dotenv
import pdfplumber

load_dotenv()

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5501"],  # Allow the frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

openai.api_key = os.getenv("OPENAI_key")
def extract_text_from_pdf(file):
    text = ""
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        return f"Error extracting text from PDF: {str(e)}"

def generate_questions(text):
    try:
        prompt = (f"Create 10 questions in each of the following sections "
                  f"based on the content:\n{text}\n"
                  "Beginner-friendly questions:\n"
                  "Intermediate-level questions:\n"
                  "Proficient-level questions\n")
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.7
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"OpenAI API error: {str(e)}"

def generate_answer(question, text):
    try:
        prompt = (f"Answer the following question based on this content in simple, understandable, and concise terms:\n"
                  f" {text}\nQuestion: {question}\nAnswer:")
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"OpenAI API error: {str(e)}"



@app.post("/upload")
async def create_upload_file(file: UploadFile = File(...)):
    if file.filename.endswith('.pdf'):
        try:
            pdf_text = extract_text_from_pdf(file.file)
            questions = generate_questions(pdf_text)
            q_and_a = {}
            for question in questions.split('\n'):
                if question.strip():
                    answer = generate_answer(question, pdf_text)
                    q_and_a[question] = answer
            return {"questions_and_answers": q_and_a}
        except Exception as e:
            return {"error": str(e)}
    else:
        return {"error": "Unsupported file type"}