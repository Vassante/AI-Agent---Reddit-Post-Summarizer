#!/usr/bin/env python3
"""
Reddit Summarizer Agent - Main Application
A chatbot that scrapes Reddit data and provides intelligent summaries
"""

import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        ('streamlit', 'streamlit'),
        ('requests', 'requests'),
        ('beautifulsoup4', 'bs4'),
        ('nltk', 'nltk')
    ]
    
    missing_packages = []
    
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install them with:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    return True

def setup_nltk_data():
    """Download required NLTK data"""
    try:
        import nltk
        
        # Check if data is already downloaded
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
            print("✅ NLTK data already available")
            return True
        except LookupError:
            pass
        
        print("📥 Downloading NLTK data...")
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        print("✅ NLTK data downloaded successfully")
        return True
        
    except Exception as e:
        print(f"⚠️ Warning: Could not download NLTK data: {e}")
        print("   The app will use a simple summarizer instead")
        return False

def main():
    """Main application entry point"""
    print("🤖 Reddit Summarizer Agent")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install missing dependencies and try again")
        return
    
    # Setup NLTK data
    setup_nltk_data()
    
    # Launch Streamlit app
    print("\n🚀 Starting Reddit Summarizer Agent...")
    print("📱 The app will open in your default web browser")
    print("🔗 If it doesn't open automatically, go to: http://localhost:8501")
    print("\n⏹️ Press Ctrl+C to stop the application")
    
    try:
        import subprocess
        import sys
        
        # Get the path to the streamlit app
        app_path = Path(__file__).parent / "streamlit_app.py"
        
        # Launch Streamlit using subprocess
        cmd = [sys.executable, "-m", "streamlit", "run", str(app_path), "--server.port", "8501", "--server.address", "localhost"]
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        print("💡 Try running: streamlit run streamlit_app.py")

if __name__ == "__main__":
    main()
