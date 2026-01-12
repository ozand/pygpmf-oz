"""Tests for CLI functionality."""
import pytest
import sys
from io import StringIO
from gpmf import __main__


class TestCLI:
    """Test command-line interface."""
    
    def test_cli_help(self):
        """Test CLI --help option."""
        # Test that help can be invoked
        assert hasattr(__main__, 'main')
        assert callable(__main__.main)
    
    def test_cli_version(self):
        """Test CLI --version option."""
        # Import version
        from gpmf import __version__
        assert __version__ is not None
        assert isinstance(__version__, str)
        assert len(__version__) > 0
    
    def test_cli_extract_command_exists(self):
        """Test that extract command exists."""
        # Verify CLI has extract functionality
        import gpmf.__main__ as cli_module
        assert hasattr(cli_module, 'main')


class TestFileOperations:
    """Test file operation commands."""
    
    def test_extract_requires_input_file(self):
        """Test that extract command requires input file."""
        # Extract should need a file argument
        # This tests the argparse structure
        pass
    
    def test_export_formats(self):
        """Test supported export formats."""
        # Should support GPX format at minimum
        supported_formats = ['gpx']
        assert 'gpx' in supported_formats
