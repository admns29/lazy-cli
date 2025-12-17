# lazy-cli Architecture Overview

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         USER                                │
│                           │                                 │
│                           ▼                                 │
│                    ┌──────────┐                             │
│                    │   lazy   │  CLI Entry Point            │
│                    └──────────┘                             │
│                           │                                 │
└───────────────────────────┼─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      MAIN.PY                                │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  • Initialize Typer App                              │   │
│  │  • Load Configuration                                │   │
│  │  • Call Plugin Loader                                │   │
│  │  • Register Commands                                 │   │
│  └──────────────────────────────────────────────────────┘   │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   PLUGIN LOADER                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │     Auto-Discovery Process:                          │   │
│  │  1. Scan plugins/ directory                          │   │
│  │  2. Import each .py file                             │   │
│  │  3. Check for PLUGIN_NAME                            │   │
│  │  4. Check for 'app' or 'main'                        │   │
│  │  5. Register as command                              │   │
│  └──────────────────────────────────────────────────────┘   │
└───────────────┬───────────┬────────────┬────────────────────┘
                │           │            │
        ┌───────▼───┐   ┌──▼──┐    ┌───▼────┐
        │ Plugin 1  │   │ ... │    │Plugin N│
        └───────────┘   └─────┘    └────────┘
                │           │            │
                └───────────┴────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   CORE UTILITIES                            │
│  ┌──────────────┬──────────────┬──────────────────────┐     │
│  │   CONFIG     │   UTILS      │   RICH CONSOLE       │     │
│  │              │              │                      │     │
│  │ • Load/Save  │ • Confirm    │ • Tables             │     │
│  │ • Pydantic   │ • Print      │ • Progress           │     │
│  │ • YAML       │ • Files      │ • Colors             │     │
│  └──────────────┴──────────────┴──────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔌 Plugin Lifecycle

```
┌────────────────────────────────────────────────────────────┐
│  1. PLUGIN FILE CREATION                                   │
│     plugins/my_plugin.py                                   │
│                                                            │
│     PLUGIN_NAME = "my-cmd"                                 │
│     PLUGIN_HELP = "Description"                            │
│     def main(): ...                                        │
└──────────────────────┬─────────────────────────────────────┘
                       │
                       │ Auto-discovery
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  2. IMPORT & VALIDATION                                     │
│     • Import module                                         │
│     • Validate PLUGIN_NAME exists                           │
│     • Validate 'app' or 'main' exists                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ Registration
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  3. COMMAND REGISTRATION                                    │
│     • Add to main Typer app                                 │
│     • Generate --help automatically                         │
│     • Setup argument parsing                                │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ User runs command
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  4. EXECUTION                                               │
│     lazy my-cmd [args] [options]                            │
│     • Parse arguments                                       │
│     • Validate types                                        │
│     • Execute plugin logic                                  │
│     • Return exit code                                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Data Flow Example: Organize Command

```
User Input:
  lazy organize ~/Downloads --dry-run

         │
         ▼
┌─────────────────────┐
│   Main Entry Point  │
│    (main.py)        │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Plugin Loader      │
│  Find 'organize'    │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  organize_files.py  │
│  main() function    │
└─────────┬───────────┘
          │
          ├─► Scan Directory
          │   └─► List all files
          │
          ├─► Categorize Files
          │   └─► By extension
          │
          ├─► Display Table
          │   └─► Rich table output
          │
          ├─► Confirm
          │   └─► (skipped if --yes)
          │
          └─► Organize (if not --dry-run)
              └─► Move files to folders
                  └─► Report results
```

---

## 🎯 Plugin Structure

```
plugins/organize_files.py
│
├─► Module Docstring
│   "What this plugin does"
│
├─► Imports
│   • typer, Path, Rich, etc.
│   • Core utilities
│
├─► Plugin Metadata
│   • PLUGIN_NAME = "organize"
│   • PLUGIN_HELP = "Organize files..."
│
├─► Helper Functions (optional)
│   • get_category()
│   • scan_directory()
│   • organize_files()
│
├─► Main Command
│   @app.command()
│   def main(...):
│       """Command logic"""
│
├─► Subcommands (optional)
│   @app.command()
│   def subcommand():
│       """Additional commands"""
│
└─► Test Entry Point
    if __name__ == "__main__":
        app()
```

---

## 🔄 Configuration Flow

```
User Config File
~/.lazy-cli/config.yaml
       │
       ▼
┌──────────────────┐
│  config.py       │
│  • Load YAML     │
│  • Pydantic      │
│  • Validate      │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐      ┌──────────────┐
│  LazyConfig      │─────►│   Plugins    │
│  • defaults      │      │  Use config  │
│  • user settings │      │  values      │
└──────────────────┘      └──────────────┘
```

---

## 🧪 Testing Architecture

```
tests/
  │
  ├─► test_plugin_loader.py
  │   • Test auto-discovery
  │   • Test plugin loading
  │   • Test get_plugin_info()
  │
  └─► test_plugins/
      │
      └─► test_organize_files.py
          • Test categorization
          • Test file scanning
          • Test dry-run mode
          • Test actual organizing
          • Test error handling
```

---

## 🎨 Rich Output Components

```
Console Output Stack:
┌─────────────────────────────────────┐
│  Rich Console                       │
│  └─► Styled Text                    │
│      • [green]Success[/green]       │
│      • [red]Error[/red]             │
│      • [yellow]Warning[/yellow]     │
│                                     │
│  └─► Tables                         │
│      • Headers                      │
│      • Rows with styling            │
│      • Borders                      │
│                                     │
│  └─► Progress Bars                  │
│      • Spinner                      │
│      • Percentage                   │
│      • Time remaining               │
│                                     │
│  └─► Panels                         │
│      • Boxed messages               │
│      • Titles                       │
│      • Borders                      │
└─────────────────────────────────────┘
```

---

## 🔐 Type Safety Flow

```
Function Definition:
  def main(file: Path, count: int = 10):

         │
         ▼
  Typer Auto-Validation:
    • Path must exist
    • int must be numeric
    • Defaults applied
         │
         ▼
  Runtime Checks:
    • Custom validation
    • Business logic
    • Error handling
         │
         ▼
  Return Type:
    • Exit code (0 = success)
    • Rich output
```

---

## 📊 Component Dependencies

```
main.py
  ├─► typer
  ├─► rich
  └─► plugin_loader
        ├─► importlib
        └─► inspect

plugin_loader
  ├─► pathlib
  ├─► typer
  └─► rich

config.py
  ├─► pydantic
  ├─► yaml
  └─► pathlib

utils.py
  ├─► typer
  ├─► rich
  └─► pathlib

Plugins
  ├─► typer
  ├─► rich
  ├─► pathlib
  ├─► utils
  └─► config (optional)
```

---

## 🚀 Execution Flow Summary

1. **User runs** `lazy organize ~/Downloads`
2. **main.py** initializes Typer app
3. **plugin_loader** scans plugins/ and finds organize_files.py
4. **plugin_loader** imports and registers organize plugin
5. **Typer** parses command line arguments
6. **organize_files.main()** is executed
7. **Plugin logic** runs (scan, categorize, display, organize)
8. **Rich** renders beautiful output
9. **Exit code** returned to shell

---

## 💡 Key Design Patterns

### 1. **Plugin Pattern**

- Plugins are self-contained modules
- Auto-discovered at runtime
- No central registration required

### 2. **Dependency Injection**

- Core utilities provided
- Plugins can import what they need
- Loose coupling

### 3. **Convention over Configuration**

- PLUGIN_NAME and PLUGIN_HELP = auto-registered
- Standard structure = auto-works
- Minimal boilerplate

### 4. **Progressive Enhancement**

- Start simple (single function)
- Add features as needed (subcommands, helpers)
- Scale complexity gradually

---

This architecture ensures:
✅ **Easy to extend** - Add new plugins without touching core
✅ **Type-safe** - Full type hints throughout
✅ **Testable** - Each component isolated
✅ **Beautiful** - Rich output by default
✅ **Maintainable** - Clear separation of concerns
