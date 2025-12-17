# Plugin Development Guide

This guide provides detailed information about developing plugins for lazy-cli.

---

## 📖 Table of Contents

- [Plugin Architecture](#plugin-architecture)
- [Plugin Structure](#plugin-structure)
- [Plugin Metadata](#plugin-metadata)
- [Command Implementation](#command-implementation)
- [Using Utilities](#using-utilities)
- [Working with Files](#working-with-files)
- [Rich Output](#rich-output)
- [Error Handling](#error-handling)
- [Testing](#testing)
- [Examples](#examples)

---

## 🏗️ Plugin Architecture

lazy-cli uses a **plugin-based architecture** where:

1. Each plugin is a **separate Python file** in `lazy_cli/plugins/`
2. Plugins are **automatically discovered** at runtime
3. Each plugin becomes a **CLI command** (or set of commands)
4. No registration required - just create the file!

### How It Works

1. When `lazy` is run, the plugin loader scans `lazy_cli/plugins/`
2. It imports each `.py` file (except `__init__.py` and `_template.py`)
3. It looks for `PLUGIN_NAME` and either `app` or `main`
4. The plugin is registered as a command in the main CLI

---

## 📄 Plugin Structure

### Minimal Plugin

```python
"""
Plugin description
"""
import typer

PLUGIN_NAME = "hello"
PLUGIN_HELP = "Say hello"

app = typer.Typer()

@app.command()
def main(name: str):
    """Greet someone."""
    print(f"Hello, {name}!")
```

### Full Plugin Template

```python
"""
Plugin: My Awesome Plugin
Detailed description of what this plugin does.
"""

import typer
from pathlib import Path
from rich.console import Console
from lazy_cli.core.utils import (
    print_success,
    print_error,
    confirm_action,
)

# ============================================================================
# Plugin Metadata (REQUIRED)
# ============================================================================
PLUGIN_NAME = "my-plugin"
PLUGIN_HELP = "Short description for --help"

# ============================================================================
# Initialize
# ============================================================================
console = Console()
app = typer.Typer()

# ============================================================================
# Main Command
# ============================================================================
@app.command()
def main(
    target: Path = typer.Argument(..., help="Target path"),
    dry_run: bool = typer.Option(False, "--dry-run", "-d"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
):
    """
    Main command implementation.
    This docstring appears when users run: lazy my-plugin --help
    """
    try:
        # Your implementation here
        print_success("Done!")

    except Exception as e:
        print_error(f"Error: {e}")
        raise typer.Exit(1)

# ============================================================================
# Optional: Subcommands
# ============================================================================
@app.command()
def subcommand():
    """A subcommand."""
    pass

# ============================================================================
# Entry point for direct testing
# ============================================================================
if __name__ == "__main__":
    app()
```

---

## 🏷️ Plugin Metadata

### Required Constants

#### PLUGIN_NAME

```python
PLUGIN_NAME = "my-command"
```

- The command name users will type
- Use lowercase with hyphens for multi-word names
- Examples: `"organize"`, `"batch-rename"`, `"stock-price"`

#### PLUGIN_HELP

```python
PLUGIN_HELP = "Brief description of what this does"
```

- Short one-line description
- Shows up in `lazy --help`
- Keep it under 60 characters

### Optional Metadata

```python
PLUGIN_VERSION = "1.0.0"
PLUGIN_AUTHOR = "Your Name"
PLUGIN_REQUIRES = ["Pillow>=10.0.0"]  # Additional dependencies
```

---

## ⚙️ Command Implementation

### Using Typer

lazy-cli uses [Typer](https://typer.tiangolo.com/) for CLI commands.

#### Arguments

```python
@app.command()
def main(
    # Positional argument (required)
    source: Path = typer.Argument(
        ...,  # ... means required
        help="Source file or directory",
        exists=True,  # Must exist
        resolve_path=True,  # Convert to absolute path
    ),

    # Optional positional argument
    destination: Path = typer.Argument(
        None,  # None means optional
        help="Destination path",
    ),
):
    pass
```

#### Options

```python
@app.command()
def main(
    # Boolean flag
    dry_run: bool = typer.Option(
        False,  # Default value
        "--dry-run", "-d",  # Long and short forms
        help="Preview without making changes",
    ),

    # String option
    format: str = typer.Option(
        "json",
        "--format", "-f",
        help="Output format (json, csv, table)",
    ),

    # Integer option
    count: int = typer.Option(
        10,
        "--count", "-n",
        help="Number of items to process",
        min=1,
        max=100,
    ),
):
    pass
```

### Type Validation

Typer automatically validates types:

```python
from pathlib import Path
from typing import Optional, List
from enum import Enum

class Format(str, Enum):
    JSON = "json"
    CSV = "csv"
    TABLE = "table"

@app.command()
def main(
    files: List[Path],  # Multiple files
    format: Format = Format.JSON,  # Enum (auto-validates)
    optional_path: Optional[Path] = None,
):
    pass
```

---

## 🛠️ Using Utilities

lazy-cli provides helpful utilities in `lazy_cli.core.utils`:

### Console Output

```python
from lazy_cli.core.utils import (
    print_success,
    print_error,
    print_warning,
    print_info,
)

print_success("Operation completed!")  # ✓ Green
print_error("Something went wrong")     # ✗ Red
print_warning("Be careful...")          # ⚠ Yellow
print_info("FYI: Some info")           # ℹ Blue
```

### User Confirmation

```python
from lazy_cli.core.utils import confirm_action

if not confirm_action("Delete all files?", default=False):
    console.print("Cancelled")
    raise typer.Exit(0)
```

### File Operations

```python
from lazy_cli.core.utils import (
    format_size,
    get_file_extension,
    ensure_directory,
    get_downloads_folder,
)

# Format file sizes
size = format_size(1536)  # "1.5 KB"

# Get extension without dot
ext = get_file_extension(Path("image.jpg"))  # "jpg"

# Create directory if needed
ensure_directory(Path("~/my-folder"))

# Get Downloads folder
downloads = get_downloads_folder()
```

---

## 📁 Working with Files

### Path Operations

```python
from pathlib import Path

# Get all files in a directory
for file in Path("/some/dir").iterdir():
    if file.is_file():
        print(file.name)

# Recursive search
for file in Path("/some/dir").rglob("*.txt"):
    print(file)

# Check file properties
path = Path("file.txt")
path.exists()         # True/False
path.is_file()       # True/False
path.is_dir()        # True/False
path.stat().st_size  # Size in bytes
```

### Moving/Copying Files

```python
import shutil
from pathlib import Path

# Move file
shutil.move(str(source), str(destination))

# Copy file
shutil.copy2(str(source), str(destination))

# Copy entire directory
shutil.copytree(str(source), str(destination))

# Remove file
Path("file.txt").unlink()

# Remove directory
shutil.rmtree(str(directory))
```

---

## 🎨 Rich Output

Use [Rich](https://rich.readthedocs.io/) for beautiful output:

### Console Printing

```python
from rich.console import Console

console = Console()

# Styled text
console.print("[bold blue]Hello[/bold blue] [green]World[/green]!")

# With emoji
console.print("✓ Success! :tada:")
```

### Tables

```python
from rich.table import Table

table = Table(title="My Table")
table.add_column("Name", style="cyan")
table.add_column("Count", justify="right", style="green")

table.add_row("Item 1", "42")
table.add_row("Item 2", "100")

console.print(table)
```

### Progress Bars

```python
from rich.progress import track

for item in track(items, description="Processing..."):
    # Do work
    pass
```

### Panels

```python
from rich.panel import Panel

console.print(Panel("Important message", title="Notice", border_style="red"))
```

---

## 🚨 Error Handling

### Basic Error Handling

```python
@app.command()
def main(file: Path):
    try:
        # Your code
        if not file.exists():
            raise FileNotFoundError(f"File not found: {file}")

        # Do work...

        print_success("Done!")

    except FileNotFoundError as e:
        print_error(str(e))
        raise typer.Exit(1)

    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise typer.Exit(1)
```

### Custom Exceptions

```python
class PluginError(Exception):
    """Base exception for this plugin."""
    pass

class ValidationError(PluginError):
    """Validation failed."""
    pass
```

---

## 🧪 Testing

### Basic Test

```python
# tests/test_plugins/test_my_plugin.py

from typer.testing import CliRunner
from lazy_cli.plugins.my_plugin import app

runner = CliRunner()

def test_my_plugin():
    result = runner.invoke(app, ["arg1", "--option"])
    assert result.exit_code == 0
    assert "Success" in result.stdout
```

### Testing with Files

```python
import tempfile
from pathlib import Path

def test_with_files():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test files
        test_file = Path(tmpdir) / "test.txt"
        test_file.write_text("Hello")

        # Run plugin
        result = runner.invoke(app, [str(test_file)])

        assert result.exit_code == 0
```

---

## 📚 Examples

### Example 1: Simple Text Processor

```python
"""Process text files."""
import typer
from pathlib import Path

PLUGIN_NAME = "process-text"
PLUGIN_HELP = "Convert text to uppercase"

@typer.command()
def main(file: Path):
    """Convert text file to uppercase."""
    text = file.read_text()
    new_text = text.upper()
    file.write_text(new_text)
    print(f"✓ Processed {file.name}")
```

### Example 2: File Counter with Table

```python
"""Count files by extension."""
import typer
from pathlib import Path
from rich.console import Console
from rich.table import Table
from collections import Counter

PLUGIN_NAME = "count-files"
PLUGIN_HELP = "Count files by extension"

console = Console()

@typer.command()
def main(directory: Path = typer.Argument(..., exists=True, file_okay=False)):
    """Count files in a directory by extension."""
    extensions = Counter()

    for file in directory.rglob("*"):
        if file.is_file():
            ext = file.suffix.lower() or "no extension"
            extensions[ext] += 1

    table = Table(title=f"Files in {directory.name}")
    table.add_column("Extension", style="cyan")
    table.add_column("Count", justify="right", style="green")

    for ext, count in extensions.most_common():
        table.add_row(ext, str(count))

    console.print(table)
```

---

## 🎓 Tips & Best Practices

1. **Use type hints** - Makes your code more maintainable
2. **Add docstrings** - Users see them in `--help`
3. **Support dry-run** - Let users preview changes
4. **Handle errors gracefully** - Don't let the app crash
5. **Use Rich** - Make your output beautiful
6. **Test your plugin** - Ensure it works correctly
7. **Keep it simple** - Each plugin should do one thing well

---

## 📖 Further Reading

- [Typer Documentation](https://typer.tiangolo.com/)
- [Rich Documentation](https://rich.readthedocs.io/)
- [Python pathlib Guide](https://docs.python.org/3/library/pathlib.html)

---

Happy plugin development! 🚀
