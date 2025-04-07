import streamlit as st
from components.sidebar import render_sidebar
from components.chat_interface import render_chat_interface
from utils.document_loader import load_document
from utils.text_processor import split_text
from utils.embeddings import create_embeddings, get_context
from utils.llm_handler import get_llm_response

def main():
    st.set_page_config(
        page_title="Document QA Bot",
        page_icon="📚",
        layout="wide"
    )
    
    # Initialize session state variables if they don't exist
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "document_text" not in st.session_state:
        st.session_state.document_text = None
    
    if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = None
    
    # Render sidebar for file upload and settings
    uploaded_file, temperature, model_name = render_sidebar()
    
    # Process uploaded file if it exists and hasn't been processed
    if uploaded_file and st.session_state.document_text is None:
        with st.spinner('Processing document...'):
            # Load document
            document_text = load_document(uploaded_file)
            st.session_state.document_text = document_text
            
            # Split text into chunks
            text_chunks = split_text(document_text)
            
            # Create vector embeddings
            st.session_state.vectorstore = create_embeddings(text_chunks)
            
            st.success(f"Document processed successfully: {uploaded_file.name}")
    
    # Render chat interface
    render_chat_interface()
    
    # Process user's question when submitted
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        if st.session_state.vectorstore is None:
            st.error("Please upload a document first.")
        else:
            user_question = st.session_state.messages[-1]["content"]
            
            with st.spinner('Thinking...'):
                # Get relevant context based on the question
                context = get_context(st.session_state.vectorstore, user_question)
                
                # Get response from LLM
                response = get_llm_response(
                    context=context,
                    question=user_question,
                    temperature=temperature,
                    model_name=model_name
                )
                
                # Add response to chat
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Force a rerun to update the UI with the new message
                st.experimental_rerun()

if __name__ == "__main__":
    main()