"""
Shared utility functions for lazy-cli plugins.
"""

from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


def confirm_action(message: str, default: bool = False) -> bool:
    """
    Ask user for confirmation before proceeding.
    
    Args:
        message: Confirmation message to display
        default: Default value if user just presses Enter
    
    Returns:
        True if user confirmed, False otherwise
    """
    return typer.confirm(message, default=default)


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[green]✓[/green] {message}")


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"[red]✗[/red] {message}")


def print_warning(message: str) -> None:
    """Print a warning message."""
    console.print(f"[yellow]⚠[/yellow] {message}")


def print_info(message: str) -> None:
    """Print an info message."""
    console.print(f"[blue]ℹ[/blue] {message}")


def create_table(title: str, columns: list[str]) -> Table:
    """
    Create a Rich table with common styling.
    
    Args:
        title: Table title
        columns: List of column headers
    
    Returns:
        Configured Rich Table instance
    """
    table = Table(title=title, show_header=True, header_style="bold magenta")
    for column in columns:
        table.add_column(column)
    return table


def format_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes: Size in bytes
    
    Returns:
        Formatted size string (e.g., "1.5 MB")
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def get_file_extension(file_path: Path) -> str:
    """
    Get file extension without the dot.
    
    Args:
        file_path: Path to file
    
    Returns:
        File extension (lowercase, without dot)
    """
    return file_path.suffix.lower().lstrip(".")


def ensure_directory(directory: Path) -> None:
    """
    Ensure a directory exists, create if it doesn't.
    
    Args:
        directory: Path to directory
    """
    directory.mkdir(parents=True, exist_ok=True)


def get_downloads_folder() -> Optional[Path]:
    """
    Get the user's Downloads folder path.
    
    Returns:
        Path to Downloads folder or None if not found
    """
    # Try common locations
    downloads_paths = [
        Path.home() / "Downloads",
        Path.home() / "downloads",
    ]
    
    for path in downloads_paths:
        if path.exists() and path.is_dir():
            return path
    
    return None


def create_progress() -> Progress:
    """
    Create a Rich progress bar with common styling.
    
    Returns:
        Configured Progress instance
    """
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    )
