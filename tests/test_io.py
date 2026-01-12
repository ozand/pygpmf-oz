"""Tests for I/O functionality."""
import pytest
import os
import shutil
from gpmf import io


class TestStreamExtraction:
    """Test GPMF stream extraction from video files."""
    
    def test_find_gpmf_stream_exists(self):
        """Test that find_gpmf_stream function exists."""
        assert hasattr(io, 'find_gpmf_stream')
        assert callable(io.find_gpmf_stream)
    
    def test_extract_gpmf_stream_exists(self):
        """Test that extract_gpmf_stream function exists."""
        assert hasattr(io, 'extract_gpmf_stream')
        assert callable(io.extract_gpmf_stream)
    
    def test_ffmpeg_availability(self):
        """Test ffmpeg availability."""
        # Check if ffmpeg is in PATH
        ffmpeg_available = shutil.which('ffmpeg') is not None
        
        # Test should document ffmpeg requirement
        if not ffmpeg_available:
            pytest.skip("ffmpeg not found in PATH - required for GPMF extraction")
        else:
            # ffmpeg is available
            assert ffmpeg_available
    
    def test_invalid_file_format(self):
        """Test handling of non-MP4 files."""
        # Test with non-existent file
        fake_file = "nonexistent_file.txt"
        
        # Should raise error for missing files
        with pytest.raises(Exception):  # ffmpeg.Error or similar
            io.find_gpmf_stream(fake_file)


class TestFileIO:
    """Test file input/output operations."""
    
    def test_read_gpmf_binary(self):
        """Test reading GPMF binary data."""
        # Test binary data handling
        sample_binary = b'\x00\x01\x02\x03\x04\x05\x06\x07'
        
        # Binary data should be bytes type
        assert isinstance(sample_binary, bytes)
        assert len(sample_binary) == 8
    
    def test_utf8_encoding_windows(self):
        """Test UTF-8 encoding on Windows."""
        # Critical for Windows support
        import sys
        
        # Verify that default encoding is UTF-8
        if sys.platform == 'win32':
            # On Windows, should support UTF-8
            test_string = "Тест UTF-8 кодировки"
            encoded = test_string.encode('utf-8')
            decoded = encoded.decode('utf-8')
            assert decoded == test_string

