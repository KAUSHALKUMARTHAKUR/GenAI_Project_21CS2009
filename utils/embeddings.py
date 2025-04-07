import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class SimpleVectorStore:
    """A simple vector store implementation using TF-IDF and cosine similarity"""
    
    def __init__(self, texts):
        """Initialize with text chunks"""
        self.texts = texts
        self.vectorizer = TfidfVectorizer(lowercase=True, stop_words='english')
        self.vectors = self.vectorizer.fit_transform(texts)
    
    def similarity_search(self, query, k=4):
        """Find the most similar documents to the query"""
        # Vectorize the query
        query_vector = self.vectorizer.transform([query])
        
        # Calculate similarities
        similarities = cosine_similarity(query_vector, self.vectors)[0]
        
        # Get top k indices
        top_indices = np.argsort(similarities)[-k:][::-1]
        
        # Create document-like objects
        results = []
        for idx in top_indices:
            results.append(SimpleDocument(self.texts[idx]))
            
        return results


class SimpleDocument:
    """A simple document class to mimic LangChain's document structure"""
    
    def __init__(self, content):
        self.page_content = content


def create_embeddings(text_chunks):
    """
    Create a simple vector store from text chunks using TF-IDF
    
    Args:
        text_chunks (list): List of text chunks
        
    Returns:
        SimpleVectorStore: Vector store with document embeddings
    """
    # Create vector store
    vectorstore = SimpleVectorStore(text_chunks)
    
    return vectorstore

def get_context(vectorstore, query, k=4):
    """
    Retrieve the most relevant context from the vector store
    
    Args:
        vectorstore: The vector store containing document embeddings
        query (str): The user question
        k (int): Number of relevant chunks to retrieve
        
    Returns:
        str: Combined relevant context
    """
    # Search for relevant chunks
    relevant_chunks = vectorstore.similarity_search(
        query=query,
        k=k
    )
    
    # Combine chunks into a single context string
    context = "\n\n".join([doc.page_content for doc in relevant_chunks])
    
    return context