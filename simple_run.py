import os
import subprocess
import sys

print("SkySecure AI Assistant")
print("=" * 30)

# Check if streamlit is installed
try:
    import streamlit
    print("✅ Streamlit found")
except ImportError:
    print("📦 Installing Streamlit...")
    subprocess.run([sys.executable, "-m", "pip", "install", "streamlit"])

# Check environment
if os.path.exists(".env"):
    print("✅ Environment file found")
else:
    print("⚠️  Create .env file with your Azure OpenAI credentials")

print("\n🚀 Starting frontend...")
print("Opening: http://localhost:8501")
print("Press Ctrl+C to stop")

# Run streamlit
subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])