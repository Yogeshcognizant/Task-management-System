#!/usr/bin/env python3
"""
Outlook AI Assistant - Multi-mode Runner
Supports Streamlit frontend and Flask API backend
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements_langchain.txt"])

def run_streamlit():
    """Run Streamlit frontend"""
    print("🚀 Starting Streamlit frontend...")
    print("Open your browser to: http://localhost:8501")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])

def run_flask_api():
    """Run Flask API backend"""
    print("🚀 Starting Flask API backend...")
    print("API available at: http://localhost:5000")
    subprocess.run([sys.executable, "langchain_backend.py"])

def check_env():
    """Check environment variables"""
    required_vars = [
        "AZURE_OPENAI_KEY",
        "AZURE_OPENAI_ENDPOINT", 
        "GRAPH_ACCESS_TOKEN"
    ]
    
    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
    
    if missing:
        print("❌ Missing environment variables:")
        for var in missing:
            print(f"   - {var}")
        print("\n💡 Create a .env file with these variables")
        return False
    
    print("✅ All environment variables found")
    return True

def main():
    print("🤖 Outlook AI Assistant")
    print("=" * 40)
    
    # Check if .env exists
    if not Path(".env").exists():
        print("⚠️  No .env file found. Copy .env.example to .env and fill in your credentials.")
    
    # Check environment
    if not check_env():
        return
    
    print("\nChoose mode:")
    print("1. Streamlit Frontend (Recommended)")
    print("2. Flask API Backend")
    print("3. Install Requirements Only")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        run_streamlit()
    elif choice == "2":
        run_flask_api()
    elif choice == "3":
        install_requirements()
        print("✅ Requirements installed!")
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()