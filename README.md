# 🚀 lazy-cli: Life Automation CLI

**Automate boring digital chores with simple, powerful commands.**

`lazy-cli` is a modular, plugin-based command-line tool that helps you automate repetitive tasks like organizing files, cleaning up downloads, converting images, and much more. Python makes automation easy, and lazy-cli makes it even easier!

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## ✨ Features

- 🔌 **Plugin-based architecture** - Each command is a separate plugin
- 🎨 **Beautiful terminal output** - Uses Rich for stunning visuals
- 🚀 **Easy to extend** - Add new commands by creating a simple Python file
- 💡 **Beginner-friendly** - Perfect for learning Python automation
- 🔧 **Type-safe** - Built with Typer for excellent CLI experience
- 📦 **No boilerplate** - Auto-discovers plugins automatically

---

## 🎯 Available Commands

| Command           | Description                              | Difficulty |
| ----------------- | ---------------------------------------- | ---------- |
| `organize`        | Organize files into folders by extension | 🟢 Easy    |
| More coming soon! |                                          |            |

---

## 📦 Installation

### Option 1: Install from source (Development)

```bash
# Clone the repository
git clone https://github.com/yourusername/lazy-cli.git
cd lazy-cli

# Install dependencies
pip install -r requirements.txt

# Install in editable mode
pip install -e .
```

### Option 2: Install from PyPI (when released)

```bash
pip install lazy-cli
```

---

## 🚀 Quick Start

Once installed, you can use the `lazy` command:

```bash
# See all available commands
lazy --help

# Get help for a specific command
lazy organize --help

# Organize files in a directory
lazy organize ~/Downloads

# Preview changes without moving files (dry run)
lazy organize ~/Downloads --dry-run

# Check version
lazy --version
```

---

## 📖 Usage Examples

### Organize Files

```bash
# Organize files in Downloads folder
lazy organize ~/Downloads

# Preview without making changes
lazy organize ~/Downloads --dry-run

# Include hidden files
lazy organize ~/Downloads --include-hidden

# Skip confirmation prompt
lazy organize ~/Downloads --yes
```

---

## 🧩 Creating Your Own Plugin

Want to add a new command? It's super easy! Just create a new Python file in `lazy_cli/plugins/`:

```python
# lazy_cli/plugins/my_plugin.py
"""
My custom plugin
"""
import typer
from rich.console import Console

PLUGIN_NAME = "hello"
PLUGIN_HELP = "Say hello to someone"

console = Console()
app = typer.Typer()

@app.command()
def main(name: str = typer.Argument(..., help="Name to greet")):
    """Greet someone by name."""
    console.print(f"[bold green]Hello, {name}![/bold green]")

if __name__ == "__main__":
    app()
```

That's it! Your new command is ready:

```bash
lazy hello World
# Output: Hello, World!
```

For more details, see our [Contributing Guide](docs/CONTRIBUTING.md) and [Plugin Development Guide](docs/PLUGIN_GUIDE.md).

---

## 🛠️ Development

### Setting up development environment

```bash
# Clone the repo
git clone https://github.com/yourusername/lazy-cli.git
cd lazy-cli

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dev dependencies
pip install -r requirements.txt

# Run tests
pytest

# Run linting
ruff check .

# Format code
black .
```

### Project Structure

```
lazy-cli/
├── lazy_cli/           # Main package
│   ├── core/          # Core system (plugin loader, config, utils)
│   ├── plugins/       # All plugins live here
│   └── main.py        # CLI entry point
├── tests/             # Unit tests
├── docs/              # Documentation
└── pyproject.toml     # Project configuration
```

---

## 🤝 Contributing

We love contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a new branch** (`git checkout -b feature/amazing-plugin`)
3. **Make your changes**
4. **Run tests** (`pytest`)
5. **Commit your changes** (`git commit -m 'Add amazing plugin'`)
6. **Push to the branch** (`git push origin feature/amazing-plugin`)
7. **Open a Pull Request**

See our [Contributing Guide](docs/CONTRIBUTING.md) for more details.

### Good First Issues

Looking for a place to start? Check out our issues labeled `good first issue`:

- [ ] Add `clean-downloads` plugin
- [ ] Add `batch-rename` plugin
- [ ] Add `backup-files` plugin
- [ ] Improve documentation
- [ ] Add more tests

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 💡 Inspiration

This project was inspired by the idea that Python is the perfect language for automating everyday tasks. We wanted to create a tool where:

- **Beginners** can write their first useful automation script
- **Contributors** can easily add new features
- **Users** get a delightful CLI experience

---

## 🙏 Acknowledgments

- Built with [Typer](https://typer.tiangolo.com/) - Amazing CLI framework
- Styled with [Rich](https://rich.readthedocs.io/) - Beautiful terminal output
- Powered by the Python community ❤️

---

## 📬 Contact

- **Issues**: [GitHub Issues](https://github.com/yourusername/lazy-cli/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/lazy-cli/discussions)

---

<div align="center">
  <strong>Made with ❤️ by the lazy-cli community</strong>
</div>
