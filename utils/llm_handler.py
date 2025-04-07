import os
import re
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI

# Load environment variables
load_dotenv()

def get_llm_response(context, question, temperature=0.3, model_name="gpt-3.5-turbo"):
    """
    Get response from the LLM based on the document context and user question
    
    Args:
        context (str): Relevant document context
        question (str): User question
        temperature (float): Model temperature (randomness)
        model_name (str): Name of the LLM model to use
        
    Returns:
        str: LLM response
    """
    # Check if OpenAI API key is available and valid
    openai_api_key = os.getenv("OPENAI_API_KEY")
    use_openai = openai_api_key and openai_api_key.startswith("sk-")
    
    system_prompt = """You are a helpful assistant that answers questions based on the provided document context.
    
Answer the user's question based ONLY on the provided context. If the answer is not contained within the context, say "I don't have enough information in the document to answer this question." Don't use prior knowledge.

Provide specific information from the context whenever possible. If quoting directly, use quotation marks.

Context:
{context}"""
    
    try:
        if use_openai:
            # Initialize OpenAI client
            client = OpenAI(api_key=openai_api_key)
            
            # Create messages
            messages = [
                {"role": "system", "content": system_prompt.format(context=context)},
                {"role": "user", "content": question}
            ]
            
            # Get response from OpenAI
            response = client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=500
            )
            
            return response.choices[0].message.content
        else:
            # Use a basic keyword matching when no valid API key is present
            return manually_generate_response(context, question)
            
    except Exception as e:
        st.error(f"Error with LLM: {str(e)}")
        # Fallback to manual response generation
        return manually_generate_response(context, question)

def manually_generate_response(context, question):
    """
    Generate a simple response without using an external LLM API
    This is a fallback when the OpenAI API is not available
    
    Args:
        context (str): Relevant document context
        question (str): User question
        
    Returns:
        str: Generated response
    """
    # Simplify question for keyword matching
    question_lower = question.lower()
    context_lower = context.lower()
    
    # Remove common stop words for better matching
    stop_words = {"the", "a", "an", "in", "on", "at", "to", "for", "with", "by", "about", "from", "of", "and", "or"}
    question_words = [word for word in re.findall(r'\b\w+\b', question_lower) if word not in stop_words and len(word) > 2]
    
    # Create sentences from context
    sentences = re.split(r'(?<=[.!?])\s+', context)
    
    # Find relevant sentences
    relevant_sentences = []
    for sentence in sentences:
        sentence_lower = sentence.lower()
        # Count matching keywords in the sentence
        match_count = sum(1 for word in question_words if word in sentence_lower)
        if match_count > 0:
            # Add as tuple with match count for later sorting
            relevant_sentences.append((match_count, sentence))
    
    # Sort by relevance and take top 3
    relevant_sentences.sort(reverse=True)
    top_sentences = [sentence for _, sentence in relevant_sentences[:3]]
    
    if top_sentences:
        response = " ".join(top_sentences)
        return f"{response}\n\nThis response was generated using keyword matching because no OpenAI API key was provided. For better answers, please provide a valid OpenAI API key."
    
    # Default response if we couldn't find relevant info
    return "I don't have enough information in the document to answer this question accurately. This response was generated using keyword matching because no OpenAI API key was provided. For better answers, please provide a valid OpenAI API key."