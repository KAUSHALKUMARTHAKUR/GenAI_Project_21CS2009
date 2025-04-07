# LLM-based Document QA Bot

A Streamlit application that allows users to upload PDF or DOCX documents and ask questions about their content. The application uses Large Language Models (LLMs) to generate responses based on the document content.

## Features

- Upload PDF or DOCX documents
- Process and index document content
- Ask questions about the document content
- Get AI-generated responses based on the document context

## Prerequisites

- Python 3.8 or higher
- OpenAI API key

## Installation

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Create a `.env` file in the project root and add your OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

1. Run the Streamlit application:
```bash
streamlit run main.py
```
2. Open your web browser and go to the URL shown in the terminal (usually http://localhost:8501)
3. Upload a PDF or DOCX document using the sidebar
4. Ask questions in the chat interface
5. The application will generate responses based on the document content

## Project Structure

- `main.py`: Main application entry point
- `components/`: UI components
  - `sidebar.py`: Sidebar with file upload and settings
  - `chat_interface.py`: Chat interface component
- `utils/`: Utility functions
  - `document_loader.py`: Functions to load PDF/DOCX documents
  - `text_processor.py`: Text preprocessing functions
  - `embeddings.py`: Generate and store embeddings
  - `llm_handler.py`: Interface with LLM API

## How it Works

1. The user uploads a document (PDF or DOCX)
2. The document is processed and text is extracted
3. The text is split into smaller chunks
4. Vector embeddings are created for each chunk
5. When the user asks a question, the system finds the most relevant chunks
6. The relevant context and the question are sent to the LLM
7. The LLM generates a response based on the provided context
8. The response is displayed to the user

## Customization

- Change the LLM model in the sidebar
- Adjust the temperature parameter to control response randomness
- Modify chunk sizes in `text_processor.py` for different document types