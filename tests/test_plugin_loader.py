"""
Tests for plugin loader functionality.
"""

import pytest
from pathlib import Path
from lazy_cli.core.plugin_loader import get_plugin_info


def test_get_plugin_info():
    """Test that plugin info can be retrieved."""
    plugins = get_plugin_info()
    
    # Should be a list
    assert isinstance(plugins, list)
    
    # Each plugin should have required fields
    for plugin in plugins:
        assert "name" in plugin
        assert "help" in plugin
        assert "file" in plugin
        assert "module" in plugin


def test_organize_plugin_exists():
    """Test that the organize plugin is loaded."""
    plugins = get_plugin_info()
    plugin_names = [p["name"] for p in plugins]
    
    assert "organize" in plugin_names
