"""
Plugin Template
Copy this file to create a new plugin.

Instructions:
1. Copy this file and rename it (e.g., my_plugin.py)
2. Update PLUGIN_NAME and PLUGIN_HELP
3. Implement your logic in the main() function
4. Add any required dependencies to requirements.txt
5. Test it: lazy <plugin-name> --help
"""

import typer
from pathlib import Path
from rich.console import Console
from lazy_cli.core.utils import print_success, print_error, confirm_action

# ============================================================================
# REQUIRED: Plugin metadata
# ============================================================================
PLUGIN_NAME = "template"  # Change this to your command name
PLUGIN_HELP = "Template plugin - replace with your description"

# ============================================================================
# Initialize
# ============================================================================
console = Console()
app = typer.Typer()


# ============================================================================
# Main command
# ============================================================================
@app.command()
def main(
    # Add your arguments here
    target: Path = typer.Argument(
        ...,
        help="Target file or directory",
        exists=True,
        resolve_path=True,
    ),
    # Add your options here
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        "-d",
        help="Preview changes without executing them",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Show detailed output",
    ),
):
    """
    Main plugin function - implement your logic here.
    """
    try:
        # Show what we're doing
        console.print(f"\n[bold blue]Running {PLUGIN_NAME}...[/bold blue]\n")
        
        if verbose:
            console.print(f"Target: {target}")
            console.print(f"Dry run: {dry_run}\n")
        
        # Example: Confirm before proceeding
        if not dry_run:
            if not confirm_action("Do you want to proceed?", default=True):
                console.print("[yellow]Cancelled.[/yellow]")
                raise typer.Exit(0)
        
        # ====================================================================
        # YOUR PLUGIN LOGIC GOES HERE
        # ====================================================================
        
        # Example logic
        if dry_run:
            console.print("[yellow]DRY RUN MODE - No changes will be made[/yellow]\n")
        
        # Do your work here
        # ...
        
        # ====================================================================
        # END OF YOUR PLUGIN LOGIC
        # ====================================================================
        
        # Show success
        print_success("Operation completed successfully!")
        
    except Exception as e:
        print_error(f"An error occurred: {str(e)}")
        raise typer.Exit(1)


# ============================================================================
# Optional: Add subcommands
# ============================================================================
@app.command()
def example_subcommand():
    """
    An example subcommand.
    Users can call this with: lazy template example-subcommand
    """
    console.print("[green]This is a subcommand![/green]")


# ============================================================================
# Entry point for testing
# ============================================================================
if __name__ == "__main__":
    app()
