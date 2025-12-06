"""
Plugin Loader - Auto-discovers and loads plugins from the plugins directory.
"""

import importlib
import inspect
from pathlib import Path
from typing import Any
import typer
from rich.console import Console

console = Console()


def load_plugins(app: typer.Typer) -> None:
    """
    Automatically discover and load all plugins from the plugins directory.
    
    Each plugin should:
    1. Have a PLUGIN_NAME constant (string) - the command name
    2. Have a PLUGIN_HELP constant (string) - command description
    3. Have either:
       - An 'app' variable (Typer instance with commands)
       - A 'main' function decorated with @app.command()
    
    Args:
        app: The main Typer application instance
    """
    # Get the plugins directory path
    plugins_dir = Path(__file__).parent.parent / "plugins"
    
    if not plugins_dir.exists():
        console.print("[yellow]Warning: Plugins directory not found[/yellow]")
        return
    
    # Find all Python files in plugins directory (excluding __init__.py and _template.py)
    plugin_files = [
        f for f in plugins_dir.glob("*.py")
        if f.name not in ["__init__.py", "_template.py"]
    ]
    
    loaded_count = 0
    
    for plugin_file in plugin_files:
        try:
            # Import the plugin module
            module_name = f"lazy_cli.plugins.{plugin_file.stem}"
            module = importlib.import_module(module_name)
            
            # Check if plugin has required attributes
            if not hasattr(module, "PLUGIN_NAME"):
                console.print(
                    f"[yellow]⚠ Skipping {plugin_file.name}: Missing PLUGIN_NAME[/yellow]"
                )
                continue
            
            plugin_name = module.PLUGIN_NAME
            plugin_help = getattr(module, "PLUGIN_HELP", "No description available")
            
            # Check if plugin has a Typer app
            if hasattr(module, "app") and isinstance(module.app, typer.Typer):
                # Add the plugin's Typer app as a subcommand
                app.add_typer(
                    module.app,
                    name=plugin_name,
                    help=plugin_help,
                )
                loaded_count += 1
                console.print(f"[green]✓[/green] Loaded plugin: [bold]{plugin_name}[/bold]")
            
            # Check if plugin has a main function
            elif hasattr(module, "main") and callable(module.main):
                # Register the main function as a command
                app.command(name=plugin_name, help=plugin_help)(module.main)
                loaded_count += 1
                console.print(f"[green]✓[/green] Loaded plugin: [bold]{plugin_name}[/bold]")
            
            else:
                console.print(
                    f"[yellow]⚠ Skipping {plugin_file.name}: No 'app' or 'main' found[/yellow]"
                )
        
        except Exception as e:
            console.print(
                f"[red]✗[/red] Failed to load {plugin_file.name}: [red]{str(e)}[/red]"
            )
    
    if loaded_count == 0:
        console.print("[yellow]No plugins loaded. Add some plugins to get started![/yellow]")
    else:
        console.print(f"\n[bold green]Successfully loaded {loaded_count} plugin(s)[/bold green]\n")


def get_plugin_info() -> list[dict[str, Any]]:
    """
    Get information about all available plugins.
    
    Returns:
        List of dictionaries containing plugin metadata
    """
    plugins_dir = Path(__file__).parent.parent / "plugins"
    plugin_files = [
        f for f in plugins_dir.glob("*.py")
        if f.name not in ["__init__.py", "_template.py"]
    ]
    
    plugins_info = []
    
    for plugin_file in plugin_files:
        try:
            module_name = f"lazy_cli.plugins.{plugin_file.stem}"
            module = importlib.import_module(module_name)
            
            if hasattr(module, "PLUGIN_NAME"):
                plugins_info.append({
                    "name": module.PLUGIN_NAME,
                    "help": getattr(module, "PLUGIN_HELP", "No description"),
                    "file": plugin_file.name,
                    "module": module_name,
                })
        except Exception:
            continue
    
    return plugins_info
