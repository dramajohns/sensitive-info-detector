from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import uvicorn
from typing import Optional
import PyPDF2
import docx
import os

app = FastAPI()

@app.post("/process-document/")
async def process_document(file: UploadFile = File(...)):
    """
    Process uploaded document and extract text content.
    Supported formats: PDF, DOCX, TXT
    """
    # Save uploaded file temporarily
    file_path = os.path.join("data", file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    
    # Extract text based on file type
    if file.filename.endswith(".pdf"):
        text = extract_pdf_text(file_path)
    elif file.filename.endswith(".docx"):
        text = extract_docx_text(file_path)
    elif file.filename.endswith(".txt"):
        text = extract_txt_text(file_path)
    else:
        return JSONResponse(
            content={"error": "Unsupported file format"},
            status_code=400
        )
    
    # Clean up - remove temporary file
    os.remove(file_path)
    
    return {"text": text}

def extract_pdf_text(file_path):
    """Extract text from PDF file"""
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_docx_text(file_path):
    """Extract text from DOCX file"""
    doc = docx.Document(file_path)
    text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    return text

def extract_txt_text(file_path):
    """Extract text from TXT file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
