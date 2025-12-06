"""
Main entry point for lazy-cli.
Initializes the CLI and dynamically loads all plugins.
"""

import typer
from rich.console import Console
from lazy_cli.core.plugin_loader import load_plugins
from lazy_cli import __version__

# Initialize the main CLI app
app = typer.Typer(
    name="lazy",
    help="🚀 Life Automation CLI - Automate boring digital chores with ease!",
    add_completion=True,
    rich_markup_mode="rich",
)

console = Console()


def version_callback(value: bool):
    """Display version information."""
    if value:
        console.print(f"[bold blue]lazy-cli[/bold blue] version [green]{__version__}[/green]")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit",
    ),
):
    """
    🚀 lazy-cli: Life Automation CLI
    
    Automate boring digital chores with simple, powerful commands.
    Each command is a plugin that you can use or extend!
    
    Use [bold]lazy --help[/bold] to see all available commands.
    """
    pass


# Dynamically load all plugins
load_plugins(app)


if __name__ == "__main__":
    app()
