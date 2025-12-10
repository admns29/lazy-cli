@echo off
REM Setup script for lazy-cli (Windows)

echo ==================================
echo 🚀 lazy-cli Setup Script (Windows)
echo ==================================
echo.

REM Check Python version
echo 📋 Checking Python version...
python --version >nul 2>&1

if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

python --version
echo ✅ Python is installed
echo.

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

if errorlevel 1 (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)

echo ✅ Virtual environment created
echo.

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed
echo.

REM Install lazy-cli in editable mode
echo 🔨 Installing lazy-cli...
pip install -e .

if errorlevel 1 (
    echo ❌ Failed to install lazy-cli
    pause
    exit /b 1
)

echo ✅ lazy-cli installed
echo.

REM Test installation
echo 🧪 Testing installation...
lazy --version

if errorlevel 1 (
    echo ❌ Installation test failed
    pause
    exit /b 1
)

echo.
echo ==================================
echo ✅ Setup Complete!
echo ==================================
echo.
echo 📖 Quick Start:
echo    1. Activate the virtual environment:
echo       venv\Scripts\activate
echo.
echo    2. Try some commands:
echo       lazy --help
echo       lazy organize --help
echo.
echo    3. Test with dry-run:
echo       mkdir test-dir ^&^& cd test-dir
echo       type nul ^> file1.jpg
echo       type nul ^> file2.pdf
echo       type nul ^> file3.mp3
echo       lazy organize . --dry-run
echo.
echo 📚 Documentation:
echo    - README.md - Project overview
echo    - docs\QUICK_START.md - Installation guide
echo    - docs\PLUGIN_GUIDE.md - How to create plugins
echo.
echo Happy automating! 🎉
echo.
pause
