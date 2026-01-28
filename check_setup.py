"""
Diagnostic script to check if everything is working
Run this before starting the Streamlit app
"""

print("🔍 Checking system requirements...")
print("-" * 50)

# Check Python version
import sys
print(f"✅ Python version: {sys.version.split()[0]}")

# Check required packages
packages_to_check = [
    "streamlit",
    "langchain",
    "langchain_community",
    "sentence_transformers",
    "faiss",
    "pypdf",
    "docx2txt"
]

missing_packages = []
for package in packages_to_check:
    try:
        if package == "faiss":
            __import__("faiss")
        else:
            __import__(package)
        print(f"✅ {package} - installed")
    except ImportError:
        print(f"❌ {package} - MISSING")
        missing_packages.append(package)

print("-" * 50)

# Check Ollama
print("\n🔍 Checking Ollama...")
print("-" * 50)
try:
    import subprocess
    result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=5)
    if "gemma3:1b" in result.stdout:
        print("✅ Ollama is running")
        print("✅ gemma3:1b model found")
    else:
        print("⚠️  Ollama is running but gemma3:1b not found")
        print("   Run: ollama pull gemma3:1b")
except FileNotFoundError:
    print("❌ Ollama not found. Please install Ollama first.")
except Exception as e:
    print(f"⚠️  Could not check Ollama: {e}")

print("-" * 50)

# Summary
print("\n📋 Summary:")
print("-" * 50)
if missing_packages:
    print(f"❌ Missing packages: {', '.join(missing_packages)}")
    print(f"\n   Install with: pip install {' '.join(missing_packages)}")
else:
    print("✅ All required packages installed!")

print("\n💡 If app loads slowly:")
print("   1. Check if Ollama is running: ollama serve")
print("   2. Make sure gemma3:1b is downloaded: ollama pull gemma3:1b")
print("   3. Close other resource-heavy applications")
print("   4. Try: streamlit run app.py --server.port 8501")

print("\n🚀 To start the app:")
print("   streamlit run app.py")
print("-" * 50)
