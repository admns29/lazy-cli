"""
Plugin: Organize Files
Automatically organize files in a directory by moving them into subfolders based on their extension.
"""

import shutil
from pathlib import Path
from typing import Dict, List
import typer
from rich.console import Console
from rich.table import Table
from lazy_cli.core.utils import (
    print_success,
    print_error,
    print_warning,
    confirm_action,
    format_size,
    get_file_extension,
    ensure_directory,
)

# Plugin metadata
PLUGIN_NAME = "organize"
PLUGIN_HELP = "Organize files into folders by their extension"

# Initialize
console = Console()
app = typer.Typer()

# File type categories
FILE_CATEGORIES = {
    "Images": ["jpg", "jpeg", "png", "gif", "bmp", "svg", "webp", "ico", "tiff", "heic"],
    "Documents": ["pdf", "doc", "docx", "txt", "rtf", "odt", "xls", "xlsx", "ppt", "pptx", "csv"],
    "Videos": ["mp4", "avi", "mkv", "mov", "wmv", "flv", "webm", "m4v", "mpeg", "mpg"],
    "Audio": ["mp3", "wav", "flac", "aac", "ogg", "wma", "m4a", "opus"],
    "Archives": ["zip", "rar", "7z", "tar", "gz", "bz2", "xz", "iso"],
    "Code": ["py", "js", "java", "cpp", "c", "h", "cs", "php", "rb", "go", "rs", "swift", "kt"],
    "Web": ["html", "css", "scss", "sass", "less", "json", "xml", "yaml", "yml"],
    "Executables": ["exe", "msi", "app", "deb", "rpm", "dmg", "apk"],
    "Others": [],  # Catch-all for unrecognized types
}


def get_category(extension: str) -> str:
    """
    Determine the category for a given file extension.
    
    Args:
        extension: File extension (without dot)
    
    Returns:
        Category name
    """
    ext_lower = extension.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if ext_lower in extensions:
            return category
    return "Others"


def scan_directory(directory: Path, include_hidden: bool = False) -> Dict[str, List[Path]]:
    """
    Scan directory and categorize files.
    
    Args:
        directory: Directory to scan
        include_hidden: Whether to include hidden files
    
    Returns:
        Dictionary mapping categories to lists of files
    """
    categorized_files: Dict[str, List[Path]] = {category: [] for category in FILE_CATEGORIES}
    
    for file_path in directory.iterdir():
        # Skip directories
        if file_path.is_dir():
            continue
        
        # Skip hidden files unless specified
        if not include_hidden and file_path.name.startswith("."):
            continue
        
        # Categorize the file
        extension = get_file_extension(file_path)
        category = get_category(extension)
        categorized_files[category].append(file_path)
    
    return categorized_files


def organize_files(
    directory: Path,
    categorized_files: Dict[str, List[Path]],
    dry_run: bool = False
) -> Dict[str, int]:
    """
    Move files into category folders.
    
    Args:
        directory: Base directory
        categorized_files: Dictionary of categorized files
        dry_run: If True, don't actually move files
    
    Returns:
        Dictionary with statistics
    """
    stats = {"moved": 0, "skipped": 0, "errors": 0}
    
    for category, files in categorized_files.items():
        if not files:
            continue
        
        # Create category folder
        category_folder = directory / category
        
        if not dry_run:
            ensure_directory(category_folder)
        
        # Move files
        for file_path in files:
            try:
                destination = category_folder / file_path.name
                
                # Check if destination already exists
                if destination.exists():
                    print_warning(f"Skipping {file_path.name} (already exists in {category})")
                    stats["skipped"] += 1
                    continue
                
                if dry_run:
                    console.print(f"  [cyan]→[/cyan] Would move: {file_path.name} to {category}/")
                else:
                    shutil.move(str(file_path), str(destination))
                    console.print(f"  [green]✓[/green] Moved: {file_path.name} to {category}/")
                
                stats["moved"] += 1
            
            except Exception as e:
                print_error(f"Failed to move {file_path.name}: {str(e)}")
                stats["errors"] += 1
    
    return stats


@app.command()
def main(
    directory: Path = typer.Argument(
        ...,
        help="Directory to organize",
        exists=True,
        file_okay=False,
        resolve_path=True,
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        "-d",
        help="Preview changes without moving files",
    ),
    include_hidden: bool = typer.Option(
        False,
        "--include-hidden",
        "-h",
        help="Include hidden files (starting with .)",
    ),
    auto_confirm: bool = typer.Option(
        False,
        "--yes",
        "-y",
        help="Skip confirmation prompt",
    ),
):
    """
    Organize files in a directory by moving them into subfolders based on their extension.
    
    Files will be categorized into folders like Images, Documents, Videos, Audio, etc.
    """
    console.print(f"\n[bold blue]📂 Organizing files in:[/bold blue] {directory}\n")
    
    if dry_run:
        console.print("[yellow]🔍 DRY RUN MODE - No files will be moved[/yellow]\n")
    
    # Scan directory
    categorized_files = scan_directory(directory, include_hidden)
    
    # Count total files
    total_files = sum(len(files) for files in categorized_files.values())
    
    if total_files == 0:
        print_warning("No files found to organize.")
        raise typer.Exit(0)
    
    # Display preview table
    table = Table(title="Files to Organize", show_header=True, header_style="bold magenta")
    table.add_column("Category", style="cyan")
    table.add_column("Count", justify="right", style="green")
    table.add_column("Total Size", justify="right", style="yellow")
    
    for category, files in categorized_files.items():
        if files:
            total_size = sum(f.stat().st_size for f in files)
            table.add_row(category, str(len(files)), format_size(total_size))
    
    console.print(table)
    console.print(f"\n[bold]Total files:[/bold] {total_files}\n")
    
    # Confirm before proceeding (unless auto-confirm)
    if not dry_run and not auto_confirm:
        if not confirm_action("Proceed with organizing files?", default=True):
            console.print("[yellow]Cancelled.[/yellow]")
            raise typer.Exit(0)
    
    # Organize files
    console.print()
    stats = organize_files(directory, categorized_files, dry_run)
    
    # Display results
    console.print()
    if dry_run:
        console.print(f"[yellow]Would organize {stats['moved']} file(s)[/yellow]")
    else:
        print_success(f"Organized {stats['moved']} file(s)")
    
    if stats["skipped"] > 0:
        print_warning(f"Skipped {stats['skipped']} file(s)")
    
    if stats["errors"] > 0:
        print_error(f"Failed to move {stats['errors']} file(s)")
    
    console.print()


if __name__ == "__main__":
    app()
