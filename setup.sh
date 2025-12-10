#!/bin/bash
# Setup script for lazy-cli

echo "=================================="
echo "🚀 lazy-cli Setup Script"
echo "=================================="
echo ""

# Check Python version
echo "📋 Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python is installed"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment"
    exit 1
fi

echo "✅ Virtual environment created"
echo ""

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed"
echo ""

# Install lazy-cli in editable mode
echo "🔨 Installing lazy-cli..."
pip install -e .

if [ $? -ne 0 ]; then
    echo "❌ Failed to install lazy-cli"
    exit 1
fi

echo "✅ lazy-cli installed"
echo ""

# Test installation
echo "🧪 Testing installation..."
lazy --version

if [ $? -ne 0 ]; then
    echo "❌ Installation test failed"
    exit 1
fi

echo ""
echo "=================================="
echo "✅ Setup Complete!"
echo "=================================="
echo ""
echo "📖 Quick Start:"
echo "   1. Activate the virtual environment:"
echo "      source venv/bin/activate"
echo ""
echo "   2. Try some commands:"
echo "      lazy --help"
echo "      lazy organize --help"
echo ""
echo "   3. Test with dry-run:"
echo "      mkdir test-dir && cd test-dir"
echo "      touch file1.jpg file2.pdf file3.mp3"
echo "      lazy organize . --dry-run"
echo ""
echo "📚 Documentation:"
echo "   - README.md - Project overview"
echo "   - docs/QUICK_START.md - Installation guide"
echo "   - docs/PLUGIN_GUIDE.md - How to create plugins"
echo ""
echo "Happy automating! 🎉"
