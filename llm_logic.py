from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
import tempfile
import os

# Local lightweight model
llm = Ollama(
    model="gemma3:1b",
    temperature=0.7
)

# Embeddings for RAG - using sentence-transformers (runs locally, no Ollama model needed)
# This is a small, efficient model that works great for embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)

def get_text_response(question: str, chat_history: list = None) -> str:
    """
    Get a response from the LLM with chat history context
    
    Args:
        question: The user's question
        chat_history: List of previous messages [{"role": "user/assistant", "content": "..."}]
    
    Returns:
        The AI's response
    """
    # Build chat history context
    history_context = ""
    if chat_history:
        recent_history = chat_history[-6:]  # Last 3 exchanges (6 messages)
        for msg in recent_history:
            role = "Human" if msg["role"] == "user" else "Assistant"
            history_context += f"{role}: {msg['content']}\n"
    
    # Create prompt with history
    if history_context:
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "You are a helpful AI assistant. "
                "Answer clearly in simple language. "
                "Use bullet points when listing multiple items. "
                "Be conversational and remember the context of previous messages."
            ),
            ("human", f"Previous conversation:\n{history_context}\n\nCurrent question: {question}")
        ])
    else:
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "You are a helpful AI assistant. "
                "Answer clearly in simple language. "
                "Use bullet points when listing multiple items."
            ),
            ("human", "{question}")
        ])

    chain = prompt | llm
    
    if history_context:
        return chain.invoke({"question": question})
    else:
        return chain.invoke({"question": question})


def process_documents(uploaded_files) -> FAISS:
    """
    Process uploaded documents and create a vector store
    
    Args:
        uploaded_files: List of uploaded files from Streamlit
    
    Returns:
        FAISS vector store
    """
    documents = []
    
    for uploaded_file in uploaded_files:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        try:
            # Load document based on file type
            file_extension = uploaded_file.name.split('.')[-1].lower()
            
            if file_extension == 'pdf':
                loader = PyPDFLoader(tmp_file_path)
            elif file_extension == 'docx':
                loader = Docx2txtLoader(tmp_file_path)
            elif file_extension == 'txt':
                loader = TextLoader(tmp_file_path)
            else:
                continue
            
            # Load and add documents
            docs = loader.load()
            documents.extend(docs)
            
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)
    
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    splits = text_splitter.split_documents(documents)
    
    # Create vector store with HuggingFace embeddings
    vector_store = FAISS.from_documents(splits, embeddings)
    
    return vector_store


def get_rag_response(question: str, vector_store: FAISS, chat_history: list = None) -> str:
    """
    Get a response using RAG (Retrieval-Augmented Generation)
    
    Args:
        question: The user's question
        vector_store: FAISS vector store containing documents
        chat_history: List of previous messages
    
    Returns:
        The AI's response based on the documents
    """
    if vector_store is None:
        return "Please upload and process documents first."
    
    # Get relevant documents using similarity search
    relevant_docs = vector_store.similarity_search(question, k=3)
    context = "\n\n".join([doc.page_content for doc in relevant_docs])
    
    # Build history context
    history_text = ""
    if chat_history:
        recent_history = chat_history[-6:]  # Last 3 exchanges
        for msg in recent_history:
            role = "Human" if msg["role"] == "user" else "Assistant"
            history_text += f"{role}: {msg['content']}\n"
    
    # Create prompt with context and history
    if history_text:
        full_prompt = f"""You are a helpful AI assistant that answers questions based on the provided documents.

Context from documents:
{context}

Previous conversation:
{history_text}

Current question: {question}

Please answer based on the context provided. If the answer is not in the documents, say so clearly."""
    else:
        full_prompt = f"""You are a helpful AI assistant that answers questions based on the provided documents.

Context from documents:
{context}

Question: {question}

Please answer based on the context provided. If the answer is not in the documents, say so clearly."""
    
    # Get response
    response = llm.invoke(full_prompt)
    
    return response
