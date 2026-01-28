# 🤖 Gemma3 AI Chatbot - Enhanced Edition

A powerful, privacy-focused AI chatbot built with Streamlit, featuring chat memory, document Q&A (RAG), and a beautiful dual-theme UI. Runs 100% locally with no API keys required!

## ✨ Features

### 💬 **Chat Features**
- ✅ **Persistent Memory** - Remembers conversation context (last 3 exchanges)
- ✅ **Streaming Responses** - Typewriter effect for natural interaction
- ✅ **Dual Theme Support** - Beautiful UI in both light and dark modes
- ✅ **Chat Statistics** - Track messages and questions in real-time

### 📚 **Document Chat (RAG)**
- ✅ **Multi-Format Support** - PDF, DOCX, and TXT files
- ✅ **Smart Search** - FAISS vector database for efficient retrieval
- ✅ **Context-Aware** - Answers based on your documents with chat history
- ✅ **Multi-Document** - Process and query multiple files simultaneously

### 🎨 **UI/UX**
- ✅ **Modern Design** - Gradient backgrounds with smooth animations
- ✅ **Responsive Layout** - Works on desktop and mobile
- ✅ **Easy Mode Switching** - Toggle between chat and document modes
- ✅ **Real-Time Stats** - Monitor your conversation metrics

### 🔒 **Privacy & Performance**
- ✅ **100% Local** - All processing happens on your machine
- ✅ **No API Keys** - Completely free, no cloud dependencies
- ✅ **Fast & Efficient** - Optimized for speed with Gemma3 1B model
- ✅ **Low Resource** - Runs on modest hardware (~2GB RAM)

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- [Ollama](https://ollama.com) installed
- 2GB+ RAM available

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/bharath2957s/gemma3-chatbot.git
cd gemma3-chatbot
```

2. **Install Ollama** (if not already installed)
```bash
# Linux/macOS
curl -fsSL https://ollama.com/install.sh | sh

# Windows
# Download from https://ollama.com/download
```

3. **Pull the Gemma3 model**
```bash
ollama pull gemma3:1b
```

4. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

5. **Run the application**
```bash
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`

## 📖 Usage Guide

### Normal Chat Mode
1. The app starts in Normal Chat mode by default
2. Type your message in the chat input
3. Press Enter to send
4. The AI remembers your conversation context

**Example:**
```
You: What is Python?
AI: Python is a high-level programming language...

You: Can you give me an example?
AI: Sure! Here's a simple example based on our discussion...
```

### Document Chat Mode (RAG)
1. Click the sidebar and select "📚 Document Chat"
2. Upload your PDF, DOCX, or TXT files
3. Click "🔄 Process Documents"
4. Wait for processing to complete
5. Ask questions about your documents

**Example:**
```
You: What are the main requirements in this document?
AI: Based on the document, the main requirements are...
```

## 🛠️ Configuration

### Change the AI Model
Edit `llm_logic.py`:
```python
llm = Ollama(
    model="gemma3:1b",  # Change to: llama2, mistral, etc.
    temperature=0.7     # Adjust creativity (0.0-1.0)
)
```

### Adjust Chat History Length
Edit `llm_logic.py`:
```python
recent_history = chat_history[-6:]  # 6 = last 3 exchanges
```

### Customize Document Chunk Size
Edit `llm_logic.py`:
```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,     # Size of text chunks
    chunk_overlap=200,   # Overlap between chunks
)
```

### Modify UI Colors
Edit the `<style>` section in `app.py` to customize colors and gradients.

## 📁 Project Structure

```
gemma3-chatbot/
├── app.py                  # Main Streamlit application
├── llm_logic.py           # LLM, RAG, and document processing logic
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── QUICKSTART.md         # Quick start guide
├── check_setup.py        # System diagnostics script
└── test_rag.py           # RAG functionality test
```

## 🔧 Troubleshooting

### App won't start or black screen
```bash
# Check if Ollama is running
ollama serve

# Verify gemma3:1b is installed
ollama list

# Run diagnostics
python check_setup.py
```

### Documents won't process
```bash
# Install missing dependencies
pip install sentence-transformers torch

# Test RAG functionality
python test_rag.py
```

### Slow responses
- Use a smaller model (gemma3:1b is already optimized)
- Close other applications to free up RAM
- Reduce chat history length in settings

### Error: "this model does not support embeddings"
This has been fixed! The app now uses HuggingFace embeddings instead of Ollama embeddings.

## 📊 System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| RAM | 2GB | 4GB+ |
| Storage | 2GB | 5GB+ |
| CPU | 2 cores | 4+ cores |
| OS | Windows 10, macOS 10.15, Ubuntu 20.04 | Latest versions |

## 🎯 Use Cases

- **Personal Assistant** - General questions and conversations
- **Document Analysis** - Extract information from PDFs/documents
- **Learning Tool** - Study with your notes and textbooks
- **Code Helper** - Get coding assistance and explanations
- **Research** - Query multiple research papers simultaneously
- **Business** - Analyze contracts, reports, and documentation

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google** - Gemma3 model
- **Ollama** - Local LLM runtime
- **LangChain** - RAG framework
- **Streamlit** - Web framework
- **Hugging Face** - Sentence transformers for embeddings

## 📮 Support

- **Email**: Sbbharath81@gmail.com

## 🌟 Star History

If you find this project useful, please consider giving it a star! ⭐

## 🗺️ Roadmap

- [ ] Add support for more document formats (PPTX, HTML)
- [ ] Implement conversation export/import
- [ ] Add voice input/output
- [ ] Multi-language support
- [ ] Web scraping capabilities
- [ ] Custom prompt templates
- [ ] Model comparison mode

## 💡 Tips & Tricks

1. **Better Results**: Be specific in your questions
2. **Document Chat**: Upload related documents together
3. **Memory**: Clear chat when switching topics
4. **Performance**: Close other apps for faster responses
5. **Privacy**: All data stays on your machine

---

**Made with ❤️ by [Bharath S B]**

**⭐ Don't forget to star this repo if you find it helpful!**
