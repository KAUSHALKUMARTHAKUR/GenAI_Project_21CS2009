import streamlit as st
from pypdf import PdfReader
import docx2txt

def load_document(uploaded_file):
    """
    Load text from PDF or DOCX file
    
    Args:
        uploaded_file: The file uploaded through Streamlit
        
    Returns:
        str: Extracted text from the document
    """
    
    file_extension = uploaded_file.name.split(".")[-1].lower()
    
    try:
        if file_extension == "pdf":
            return load_pdf(uploaded_file)
        elif file_extension == "docx":
            return load_docx(uploaded_file)
        else:
            st.error(f"Unsupported file format: {file_extension}")
            return None
    except Exception as e:
        st.error(f"Error loading document: {str(e)}")
        return None

def load_pdf(file):
    """Extract text from PDF file"""
    pdf_reader = PdfReader(file)
    text = ""
    
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    
    return text

def load_docx(file):
    """Extract text from DOCX file"""
    text = docx2txt.process(file)
    return text