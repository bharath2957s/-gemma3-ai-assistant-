# 🚀 Quick Start Guide

Get up and running with Gemma3 Chatbot in under 5 minutes!

## ⚡ Super Quick Setup

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/gemma3-chatbot.git
cd gemma3-chatbot

# 2. Install Ollama (if not installed)
curl -fsSL https://ollama.com/install.sh | sh  # Linux/macOS
# For Windows: Download from https://ollama.com/download

# 3. Get the AI model
ollama pull gemma3:1b

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the app
streamlit run app.py
```

That's it! The app opens at `http://localhost:8501` 🎉

## 🎯 First Steps

### Try Normal Chat
1. Type "What is Python?" in the chat box
2. Press Enter
3. Follow up with "Can you give me an example?"
4. Notice how it remembers context!

### Try Document Chat
1. Click sidebar → Select "📚 Document Chat"
2. Upload a PDF or DOCX file
3. Click "🔄 Process Documents"
4. Ask: "What is this document about?"

## 🔧 Verify Installation

Run the diagnostic:
```bash
python check_setup.py
```

Should show all ✅ green checks!

## 🆘 Quick Fixes

### "Ollama not running"
```bash
ollama serve
```

### "Model not found"
```bash
ollama pull gemma3:1b
```

### "Import errors"
```bash
pip install -r requirements.txt --upgrade
```

### "Embeddings error"
```bash
pip install sentence-transformers torch
```

## 📱 Access Options

**Local**: http://localhost:8501  
**Network**: http://YOUR_IP:8501  
**Custom Port**: `streamlit run app.py --server.port 8080`

## 💡 Pro Tips

✅ **Faster Loading**: The first run downloads embedding model (~80MB)  
✅ **Better Answers**: Be specific in your questions  
✅ **Document Chat**: Upload related docs together  
✅ **Save Memory**: Clear chat when switching topics  

## 🎨 Customization

Want to customize? Check these files:
- `app.py` - UI and styling
- `llm_logic.py` - AI behavior
- `requirements.txt` - Dependencies

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed docs
- Check [EMBEDDINGS_FIX.md](EMBEDDINGS_FIX.md) for troubleshooting
- Run `python test_rag.py` to test RAG functionality

## 🤝 Need Help?

- **Issues**: [GitHub Issues](https://github.com/yourusername/gemma3-chatbot/issues)
- **Questions**: [Discussions](https://github.com/yourusername/gemma3-chatbot/discussions)

## 🌟 Enjoying the app?

Give us a star on GitHub! ⭐

---

**Happy Chatting! 🤖**
