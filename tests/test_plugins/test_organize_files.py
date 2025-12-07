"""
Tests for the organize_files plugin.
"""

import pytest
from pathlib import Path
import tempfile
from typer.testing import CliRunner
from lazy_cli.plugins.organize_files import app, get_category, scan_directory

runner = CliRunner()


def test_get_category():
    """Test file categorization."""
    assert get_category("jpg") == "Images"
    assert get_category("pdf") == "Documents"
    assert get_category("mp4") == "Videos"
    assert get_category("mp3") == "Audio"
    assert get_category("zip") == "Archives"
    assert get_category("py") == "Code"
    assert get_category("html") == "Web"
    assert get_category("exe") == "Executables"
    assert get_category("unknown") == "Others"


def test_scan_directory():
    """Test directory scanning."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        
        # Create test files
        (tmpdir_path / "test.jpg").touch()
        (tmpdir_path / "doc.pdf").touch()
        (tmpdir_path / "video.mp4").touch()
        
        # Scan directory
        categorized = scan_directory(tmpdir_path)
        
        # Check results
        assert len(categorized["Images"]) == 1
        assert len(categorized["Documents"]) == 1
        assert len(categorized["Videos"]) == 1


def test_organize_help():
    """Test that help text is displayed."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Organize files" in result.stdout


def test_organize_dry_run():
    """Test organize in dry-run mode."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        
        # Create test files
        (tmpdir_path / "test.jpg").touch()
        (tmpdir_path / "doc.pdf").touch()
        
        # Run in dry-run mode
        result = runner.invoke(app, [str(tmpdir_path), "--dry-run", "--yes"])
        
        # Should succeed
        assert result.exit_code == 0
        
        # Files should still be in original location
        assert (tmpdir_path / "test.jpg").exists()
        assert (tmpdir_path / "doc.pdf").exists()
        assert not (tmpdir_path / "Images").exists()
        assert not (tmpdir_path / "Documents").exists()
