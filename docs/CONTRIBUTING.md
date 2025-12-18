# Contributing to lazy-cli

Thank you for your interest in contributing to lazy-cli! 🎉

This document provides guidelines and instructions for contributing to the project.

---

## 🌟 How Can I Contribute?

There are many ways to contribute:

1. **Add New Plugins** - Create new automation commands
2. **Fix Bugs** - Help squash bugs in existing plugins
3. **Improve Documentation** - Make our docs better
4. **Report Issues** - Found a bug? Let us know!
5. **Suggest Features** - Have an idea? We'd love to hear it!

---

## 🔌 Creating a New Plugin

Creating a plugin is super easy! Follow these steps:

### Step 1: Copy the Template

```bash
cp lazy_cli/plugins/_template.py lazy_cli/plugins/my_plugin.py
```

### Step 2: Update Plugin Metadata

```python
PLUGIN_NAME = "my-command"  # This will be the command name
PLUGIN_HELP = "Description of what your plugin does"
```

### Step 3: Implement Your Logic

Edit the `main()` function:

```python
@app.command()
def main(
    # Your arguments
    target: Path = typer.Argument(..., help="Target file"),
    # Your options
    dry_run: bool = typer.Option(False, "--dry-run", "-d"),
):
    """Your command description."""
    # Your implementation here
    pass
```

### Step 4: Test Your Plugin

```bash
# Install in development mode
pip install -e .

# Test your plugin
lazy my-command --help
```

### Step 5: Add Tests

Create a test file in `tests/test_plugins/`:

```python
# tests/test_plugins/test_my_plugin.py
def test_my_plugin():
    # Your tests here
    pass
```

---

## 📋 Plugin Best Practices

### Required Elements

Every plugin MUST have:

1. **PLUGIN_NAME** - The command name (string)
2. **PLUGIN_HELP** - Short description (string)
3. **Docstring** - Explain what the plugin does
4. **Either `app` or `main`** - Typer app or main function

### Recommended Features

Good plugins should:

1. **Use Rich for output** - Makes the CLI beautiful

   ```python
   from rich.console import Console
   console = Console()
   console.print("[green]Success![/green]")
   ```

2. **Support dry-run mode** - Let users preview changes

   ```python
   dry_run: bool = typer.Option(False, "--dry-run", "-d")
   ```

3. **Ask for confirmation** - For destructive operations

   ```python
   from lazy_cli.core.utils import confirm_action
   if not confirm_action("Are you sure?"):
       raise typer.Exit(0)
   ```

4. **Handle errors gracefully** - Use try/except

   ```python
   try:
       # Your code
   except Exception as e:
       print_error(f"Error: {e}")
       raise typer.Exit(1)
   ```

5. **Provide helpful messages** - Use the utility functions
   ```python
   from lazy_cli.core.utils import print_success, print_error, print_warning
   ```

### Code Style

- Use **type hints** for all function arguments
- Follow **PEP 8** style guide
- Use **meaningful variable names**
- Add **comments** for complex logic
- Keep functions **short and focused**

### Documentation

- Add a **docstring** to your plugin module
- Document **all functions**
- Include **usage examples** in docstrings
- Update **README.md** if needed

---

## 🧪 Testing

Before submitting a PR:

1. **Run tests**:

   ```bash
   pytest
   ```

2. **Check code style**:

   ```bash
   ruff check .
   black --check .
   ```

3. **Format your code**:

   ```bash
   black .
   ```

4. **Test your plugin manually**:
   ```bash
   lazy your-command --help
   lazy your-command --dry-run
   ```

---

## 📝 Pull Request Process

1. **Fork the repository**
2. **Create a new branch**:
   ```bash
   git checkout -b feature/my-awesome-plugin
   ```
3. **Make your changes**
4. **Commit with a clear message**:
   ```bash
   git commit -m "Add my-awesome-plugin for doing X"
   ```
5. **Push to your fork**:
   ```bash
   git push origin feature/my-awesome-plugin
   ```
6. **Open a Pull Request** on GitHub
7. **Describe your changes** in the PR description
8. **Wait for review** - We'll get back to you soon!

### PR Checklist

- [ ] Plugin follows the template structure
- [ ] Code is tested and working
- [ ] Docstrings are added
- [ ] README updated (if needed)
- [ ] No linting errors
- [ ] Follows code style guidelines

---

## 💡 Plugin Ideas

Need inspiration? Here are some plugin ideas:

### Easy (Great for beginners!)

- [ ] `clean-downloads` - Delete old files from Downloads
- [ ] `batch-rename` - Rename multiple files with patterns
- [ ] `json-format` - Pretty-print JSON files
- [ ] `hash-file` - Calculate file checksums
- [ ] `qr-generate` - Generate QR codes

### Medium

- [ ] `image-resize` - Resize images
- [ ] `images-to-pdf` - Convert images to PDF
- [ ] `backup-files` - Backup folders to zip
- [ ] `git-cleanup` - Clean up old git branches
- [ ] `weather` - Show weather forecast

### Advanced

- [ ] `youtube-download` - Download YouTube videos
- [ ] `compress-pdf` - Compress PDF files
- [ ] `stock-price` - Track stock prices
- [ ] `schedule-task` - Schedule commands

---

## 🐛 Reporting Bugs

Found a bug? Please [open an issue](https://github.com/yourusername/lazy-cli/issues) with:

1. **Clear title** - Describe the bug briefly
2. **Steps to reproduce** - How to trigger the bug
3. **Expected behavior** - What should happen
4. **Actual behavior** - What actually happens
5. **Environment** - OS, Python version, etc.
6. **Error messages** - Full error output if available

---

## 💬 Questions?

- Open a [Discussion](https://github.com/yourusername/lazy-cli/discussions)
- Check existing [Issues](https://github.com/yourusername/lazy-cli/issues)
- Read the [Plugin Guide](PLUGIN_GUIDE.md)

---

## 📜 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Help each other learn
- Have fun! 🎉

---

Thank you for contributing to lazy-cli! ❤️
