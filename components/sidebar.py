import streamlit as st
import os

def render_sidebar():
    with st.sidebar:
        st.title("Document QA Bot")
        st.markdown("Upload a document and ask questions about its content.")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Upload a PDF or DOCX file", 
            type=["pdf", "docx"],
            help="Upload the document you want to query"
        )
        
        st.divider()
        
        # API Key input
        api_key = st.text_input(
            "OpenAI API Key",
            value=os.getenv("OPENAI_API_KEY", ""),
            type="password",
            help="Enter your OpenAI API key. If left empty, a free fallback method will be used."
        )
        
        if api_key:
            # Update the environment variable
            os.environ["OPENAI_API_KEY"] = api_key
        
        # LLM settings
        st.subheader("Model Settings")
        
        model_name = st.selectbox(
            "Select LLM Model",
            options=["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
            index=0,
            help="Select the language model to use for generating responses (requires valid API key)"
        )
        
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.3,
            step=0.1,
            help="Controls the randomness of responses. Lower values make responses more deterministic."
        )
        
        if uploaded_file:
            if st.button("Clear Document", type="primary"):
                # Clear document and related session state
                st.session_state.document_text = None
                st.session_state.vectorstore = None
                st.session_state.messages = []
                st.experimental_rerun()
        
        st.divider()
        
        # App info
        st.markdown("### About")
        st.markdown(
            "This app allows you to upload a document (PDF or DOCX) "
            "and ask questions about its content. The app uses LLM to "
            "generate responses based on the document content."
        )
        
        # Info about free mode
        if not api_key or not api_key.startswith("sk-"):
            st.warning(
                "⚠️ Running in free mode with limited capabilities. "
                "For better results, add your OpenAI API key."
            )
        
    return uploaded_file, temperature, model_name