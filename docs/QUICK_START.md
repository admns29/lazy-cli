# Quick Start Guide

Get started with lazy-cli in just a few minutes!

---

## 📦 Installation

### Prerequisites

- **Python 3.8 or higher** ([Download Python](https://www.python.org/downloads/))
- **pip** (comes with Python)
- **Git** (optional, for cloning)

### Step 1: Get the Code

**Option A: Clone from GitHub**

```bash
git clone https://github.com/yourusername/lazy-cli.git
cd lazy-cli
```

**Option B: Download ZIP**

1. Download the repository as ZIP
2. Extract it
3. Open terminal in the extracted folder

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# Install all dependencies
pip install -r requirements.txt

# Install lazy-cli in editable mode
pip install -e .
```

### Step 4: Verify Installation

```bash
# Check if lazy command works
lazy --version

# See available commands
lazy --help
```

You should see:

```
lazy-cli version 0.1.0
```

---

## 🎯 Your First Command

Let's try the `organize` command to organize files!

### Test it with Dry Run

Create a test directory:

```bash
# Create test directory
mkdir test-organize
cd test-organize

# Create some dummy files
touch photo1.jpg photo2.png document.pdf music.mp3 code.py
```

Preview what would happen:

```bash
lazy organize . --dry-run
```

You'll see a table showing how files would be organized!

### Actually Organize

```bash
lazy organize . --yes
```

Files are now neatly organized into folders!

---

## 🔧 Common Commands

### Organize Files

```bash
# Organize Downloads folder
lazy organize ~/Downloads

# Preview first
lazy organize ~/Downloads --dry-run

# Include hidden files
lazy organize ~/Downloads --include-hidden

# Auto-confirm (skip prompt)
lazy organize ~/Downloads --yes
```

---

## 🆘 Troubleshooting

### Command not found: lazy

**Problem:** Terminal doesn't recognize `lazy` command

**Solution:**

```bash
# Make sure you installed it
pip install -e .

# Or run directly with Python
python -m lazy_cli.main --help
```

### Import errors

**Problem:** Missing dependencies

**Solution:**

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Permission denied

**Problem:** Can't access certain directories

**Solution:**

- Run with appropriate permissions
- On Windows: Run terminal as Administrator
- On macOS/Linux: Use `sudo` if needed

---

## 🎓 Next Steps

1. **Explore Commands** - Run `lazy --help` to see all commands
2. **Create a Plugin** - Follow the [Plugin Guide](PLUGIN_GUIDE.md)
3. **Read Contributing Guide** - Check out [CONTRIBUTING.md](CONTRIBUTING.md)
4. **Join Community** - Star the repo and contribute!

---

## 📚 Learn More

- [README](../README.md) - Project overview
- [Plugin Guide](PLUGIN_GUIDE.md) - How to create plugins
- [Contributing](CONTRIBUTING.md) - How to contribute

---

Happy automating! 🚀
