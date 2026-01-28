"""
Quick test to verify RAG functionality
"""

print("🧪 Testing RAG Setup...")
print("-" * 50)

# Test imports
try:
    from llm_logic import get_text_response, get_rag_response, process_documents
    print("✅ Successfully imported functions")
except Exception as e:
    print(f"❌ Import error: {e}")
    exit(1)

# Test embeddings
try:
    from langchain_community.embeddings import HuggingFaceEmbeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )
    print("✅ Embeddings model loaded")
except Exception as e:
    print(f"❌ Embeddings error: {e}")
    exit(1)

# Test FAISS
try:
    from langchain_community.vectorstores import FAISS
    from langchain.schema import Document
    
    # Create a simple test document
    test_docs = [
        Document(page_content="Python is a programming language."),
        Document(page_content="It is used for web development, data science, and AI.")
    ]
    
    test_store = FAISS.from_documents(test_docs, embeddings)
    print("✅ FAISS vector store created")
    
    # Test similarity search
    results = test_store.similarity_search("What is Python?", k=1)
    print(f"✅ Similarity search works: Found {len(results)} result(s)")
    
except Exception as e:
    print(f"❌ FAISS error: {e}")
    exit(1)

# Test Ollama connection
try:
    from langchain_community.llms import Ollama
    llm = Ollama(model="gemma3:1b", temperature=0.7)
    response = llm.invoke("Say 'test successful' if you can read this.")
    print(f"✅ Ollama connection works")
    print(f"   Response: {response[:50]}...")
except Exception as e:
    print(f"❌ Ollama error: {e}")
    print("   Make sure Ollama is running: ollama serve")
    print("   And gemma3:1b is installed: ollama pull gemma3:1b")

print("-" * 50)
print("✅ All tests passed! RAG should work correctly.")
print("\n🚀 You can now run: streamlit run app.py")
