import streamlit as st
from llm_logic import get_text_response, get_rag_response, process_documents
import time

# Page config
st.set_page_config(
    page_title="Gemma3 AI Assistant", 
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simplified CSS with excellent readability in both themes
st.markdown("""
<style>
    /* Main background gradients */
    [data-testid="stAppViewContainer"] > div:first-child {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    @media (prefers-color-scheme: dark) {
        [data-testid="stAppViewContainer"] > div:first-child {
            background: linear-gradient(135deg, #1e3a5f 0%, #2d1b4e 100%);
        }
    }
    
    /* Sidebar - always dark */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%) !important;
    }
    
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Title - always white with strong shadow */
    h1 {
        color: white !important;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.8);
        text-align: center;
        padding: 1rem 0;
    }
    
    /* Subtitle */
    .subtitle-text {
        color: white !important;
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.6);
    }
    
    /* CHAT MESSAGES - CRITICAL FIX */
    /* User messages */
    [data-testid="stChatMessage"][class*="user"] {
        background-color: white !important;
        color: #1a1a1a !important;
        border: none !important;
    }
    
    [data-testid="stChatMessage"][class*="user"] * {
        color: #1a1a1a !important;
    }
    
    /* Assistant messages - light mode */
    [data-testid="stChatMessage"]:not([class*="user"]) {
        background-color: #f0f4ff !important;
        color: #1a1a1a !important;
        border: none !important;
    }
    
    [data-testid="stChatMessage"]:not([class*="user"]) * {
        color: #1a1a1a !important;
    }
    
    /* Dark mode chat messages */
    @media (prefers-color-scheme: dark) {
        [data-testid="stChatMessage"][class*="user"] {
            background-color: #2d3748 !important;
            color: #f7fafc !important;
            border: 1px solid #4a5568 !important;
        }
        
        [data-testid="stChatMessage"][class*="user"] * {
            color: #f7fafc !important;
        }
        
        [data-testid="stChatMessage"]:not([class*="user"]) {
            background-color: #1a202c !important;
            color: #e2e8f0 !important;
            border: 1px solid #4a5568 !important;
        }
        
        [data-testid="stChatMessage"]:not([class*="user"]) * {
            color: #e2e8f0 !important;
        }
    }
    
    /* Chat message styling */
    [data-testid="stChatMessage"] {
        border-radius: 12px;
        padding: 1.2rem;
        margin: 0.8rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 24px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background-color: rgba(255, 255, 255, 0.15);
        border-radius: 12px;
        padding: 1rem;
        border: 2px dashed rgba(255, 255, 255, 0.4);
    }
    
    [data-testid="stFileUploader"] * {
        color: white !important;
    }
    
    /* Metrics */
    [data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 0.8rem;
        border-radius: 8px;
    }
    
    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"] {
        color: white !important;
    }
    
    /* Alert boxes - LIGHT MODE */
    [data-testid="stAlert"] {
        border-radius: 10px;
        font-weight: 500;
    }
    
    /* Info */
    [data-testid="stAlert"][data-baseweb="notification"][kind="info"] {
        background-color: #dbeafe !important;
        color: #1e40af !important;
        border: 2px solid #3b82f6 !important;
    }
    
    [data-testid="stAlert"][data-baseweb="notification"][kind="info"] * {
        color: #1e40af !important;
    }
    
    /* Warning */
    [data-testid="stAlert"][data-baseweb="notification"][kind="warning"] {
        background-color: #fef3c7 !important;
        color: #92400e !important;
        border: 2px solid #f59e0b !important;
    }
    
    [data-testid="stAlert"][data-baseweb="notification"][kind="warning"] * {
        color: #92400e !important;
    }
    
    /* Success */
    [data-testid="stAlert"][data-baseweb="notification"][kind="success"] {
        background-color: #d1fae5 !important;
        color: #065f46 !important;
        border: 2px solid #10b981 !important;
    }
    
    [data-testid="stAlert"][data-baseweb="notification"][kind="success"] * {
        color: #065f46 !important;
    }
    
    /* DARK MODE Alerts */
    @media (prefers-color-scheme: dark) {
        [data-testid="stAlert"][data-baseweb="notification"][kind="info"] {
            background-color: #1e3a8a !important;
            color: #bfdbfe !important;
            border: 2px solid #3b82f6 !important;
        }
        
        [data-testid="stAlert"][data-baseweb="notification"][kind="info"] * {
            color: #bfdbfe !important;
        }
        
        [data-testid="stAlert"][data-baseweb="notification"][kind="warning"] {
            background-color: #78350f !important;
            color: #fde68a !important;
            border: 2px solid #f59e0b !important;
        }
        
        [data-testid="stAlert"][data-baseweb="notification"][kind="warning"] * {
            color: #fde68a !important;
        }
        
        [data-testid="stAlert"][data-baseweb="notification"][kind="success"] {
            background-color: #064e3b !important;
            color: #a7f3d0 !important;
            border: 2px solid #10b981 !important;
        }
        
        [data-testid="stAlert"][data-baseweb="notification"][kind="success"] * {
            color: #a7f3d0 !important;
        }
    }
    
    /* Chat input */
    [data-testid="stChatInput"] textarea {
        border-radius: 24px !important;
        border: 2px solid rgba(102, 126, 234, 0.5) !important;
        background-color: white !important;
        color: #1a1a1a !important;
    }
    
    [data-testid="stChatInput"] textarea::placeholder {
        color: #9ca3af !important;
    }
    
    @media (prefers-color-scheme: dark) {
        [data-testid="stChatInput"] textarea {
            background-color: #2d3748 !important;
            color: white !important;
            border-color: rgba(102, 126, 234, 0.7) !important;
        }
        
        [data-testid="stChatInput"] textarea::placeholder {
            color: #cbd5e0 !important;
        }
    }
    
    /* Expander */
    [data-testid="stExpander"] {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    [data-testid="stExpander"] * {
        color: white !important;
    }
    
    @media (prefers-color-scheme: dark) {
        [data-testid="stExpander"] {
            background-color: rgba(255, 255, 255, 0.05);
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "rag_enabled" not in st.session_state:
    st.session_state.rag_enabled = False

if "documents_processed" not in st.session_state:
    st.session_state.documents_processed = False

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    st.markdown("---")
    
    # Mode selection
    mode = st.radio(
        "Select Chat Mode",
        ["💬 Normal Chat", "📚 Document Chat (RAG)"],
        help="Switch between normal conversation and document-based Q&A"
    )
    
    st.session_state.rag_enabled = (mode == "📚 Document Chat (RAG)")
    
    st.markdown("---")
    
    # Document upload section (only show in RAG mode)
    if st.session_state.rag_enabled:
        st.markdown("### 📄 Upload Documents")
        
        uploaded_files = st.file_uploader(
            "Choose PDF, DOCX, or TXT files",
            type=["pdf", "docx", "txt"],
            accept_multiple_files=True,
            help="Upload documents to analyze and chat with"
        )
        
        if uploaded_files:
            st.info(f"📁 {len(uploaded_files)} file(s) selected")
            
            if st.button("🔄 Process Documents", use_container_width=True):
                with st.spinner("Processing your documents..."):
                    try:
                        st.session_state.vector_store = process_documents(uploaded_files)
                        st.session_state.documents_processed = True
                        st.success(f"✅ Successfully processed {len(uploaded_files)} document(s)!")
                        time.sleep(1)
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
        
        if st.session_state.documents_processed:
            st.success("📚 Documents ready! Ask me anything about them.")
    
    st.markdown("---")
    
    # Chat statistics
    st.markdown("### 📊 Statistics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Messages", len(st.session_state.messages))
    with col2:
        user_msgs = len([m for m in st.session_state.messages if m["role"] == "user"])
        st.metric("Questions", user_msgs)
    
    st.markdown("---")
    
    # Action buttons
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    if st.session_state.rag_enabled and st.button("🔄 Reset Documents", use_container_width=True):
        st.session_state.documents_processed = False
        st.session_state.vector_store = None
        st.rerun()
    
    st.markdown("---")
    
    # About section
    st.markdown("### ℹ️ About")
    st.caption("""
    **Model:** Gemma3 (1B)  
    **Framework:** LangChain  
    **Runtime:** Ollama  
    
    🔒 100% Local & Private  
    ⚡ Fast & Efficient  
    🆓 Completely Free
    """)

# Main chat interface
st.title("🤖 Gemma3 AI Assistant")

if st.session_state.rag_enabled:
    st.markdown('<p class="subtitle-text">📚 Document Chat Mode • Ask questions about your uploaded documents</p>', unsafe_allow_html=True)
else:
    st.markdown('<p class="subtitle-text">💬 Normal Chat Mode • General conversation with context memory</p>', unsafe_allow_html=True)

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "🤖"):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("💭 Type your message here..."):
    # Check if RAG mode is enabled but no documents uploaded
    if st.session_state.rag_enabled and not st.session_state.documents_processed:
        st.warning("⚠️ Please upload and process documents first using the sidebar!")
    else:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        
        # Get AI response
        with st.chat_message("assistant", avatar="🤖"):
            message_placeholder = st.empty()
            
            with st.spinner("🤔 Thinking..."):
                try:
                    if st.session_state.rag_enabled:
                        # RAG response
                        response = get_rag_response(
                            prompt, 
                            st.session_state.vector_store,
                            st.session_state.messages[:-1]
                        )
                    else:
                        # Normal response with chat history
                        response = get_text_response(
                            prompt,
                            st.session_state.messages[:-1]
                        )
                    
                    # Simulate streaming effect
                    full_response = ""
                    words = response.split()
                    for i, word in enumerate(words):
                        full_response += word + " "
                        if i % 3 == 0:  # Update every 3 words for smoother effect
                            time.sleep(0.03)
                            message_placeholder.markdown(full_response + "▌")
                    
                    message_placeholder.markdown(response)
                    
                except Exception as e:
                    response = f"❌ Sorry, I encountered an error: {str(e)}"
                    message_placeholder.markdown(response)
            
            # Add assistant response to chat
            st.session_state.messages.append({"role": "assistant", "content": response})

# Welcome message for new users
if len(st.session_state.messages) == 0:
    st.info("👋 **Welcome!** I'm your AI assistant powered by Gemma3. Start chatting or upload documents to begin!")
    
    with st.expander("💡 Quick Tips"):
        st.markdown("""
        **Normal Chat Mode:**
        - Ask me anything - I'll remember our conversation
        - I can help with coding, writing, analysis, and more
        
        **Document Chat Mode:**
        - Upload PDF, DOCX, or TXT files
        - Ask specific questions about your documents
        - I'll provide answers based on the content
        
        **Pro Tips:**
        - Switch modes using the sidebar
        - Clear chat history anytime
        - Your data stays 100% private and local
        """)