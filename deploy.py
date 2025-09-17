#!/usr/bin/env python3
"""
Simple deployment script for Teams Interview Bot
Run this after setting up your Azure resources
"""

import os
import subprocess
import sys
from dotenv import load_dotenv

def check_requirements():
    """Check if all required environment variables are set"""
    load_dotenv()
    
    required_vars = [
        "AZURE_OPENAI_KEY",
        "AZURE_OPENAI_ENDPOINT", 
        "MICROSOFT_APP_ID",
        "MICROSOFT_APP_PASSWORD",
        "AZURE_TENANT_ID"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set these in your .env file")
        return False
    
    print("✅ All required environment variables are set")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements_teams.txt"], check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def test_auth():
    """Test authentication with Azure services"""
    print("🔐 Testing authentication...")
    try:
        from auth_helper import GraphAuthHelper
        
        auth = GraphAuthHelper()
        token = auth.get_access_token()
        
        if token:
            print("✅ Graph API authentication successful")
            return True
        else:
            print("❌ Graph API authentication failed")
            return False
            
    except Exception as e:
        print(f"❌ Authentication test failed: {e}")
        return False

def start_bot():
    """Start the bot application"""
    print("🚀 Starting Teams Interview Bot...")
    try:
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error starting bot: {e}")

def main():
    print("🤖 Teams Interview Bot Deployment")
    print("=" * 40)
    
    # Step 1: Check environment
    if not check_requirements():
        sys.exit(1)
    
    # Step 2: Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Step 3: Test authentication
    if not test_auth():
        print("⚠️  Authentication failed, but continuing...")
        print("   Make sure your Azure resources are properly configured")
    
    # Step 4: Start bot
    print("\n🎯 Ready to start bot!")
    print("   Bot will be available at: http://localhost:3978")
    print("   Webhook endpoint: http://localhost:3978/api/messages")
    print("\nPress Ctrl+C to stop the bot\n")
    
    start_bot()

if __name__ == "__main__":
    main()