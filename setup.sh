#!/bin/bash

# Emotion-Based Music Recommendation App - Setup Script
# This script sets up the development environment and installs all dependencies

echo "🎵 Emotion-Based Music Recommendation App - Setup"
echo "=================================================="
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
echo "✅ Virtual environment created"
echo ""

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip
echo "✅ pip upgraded"
echo ""

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt
echo "✅ All dependencies installed"
echo ""

# Summary
echo "=================================================="
echo "✨ Setup Complete!"
echo "=================================================="
echo ""
echo "To start the app, run:"
echo "  source venv/bin/activate"
echo "  streamlit run app.py"
echo ""
echo "The app will open at: http://localhost:8501"
echo ""
