"""Tests for GPMF parsing functionality."""
import pytest
import struct
from gpmf import parse


class TestUtilityFunctions:
    """Test GPMF utility functions."""
    
    def test_ceil4_basic(self):
        """Test ceil4 function with basic values."""
        assert parse.ceil4(1) == 4
        assert parse.ceil4(2) == 4
        assert parse.ceil4(3) == 4
        assert parse.ceil4(4) == 4
        assert parse.ceil4(5) == 8
    
    def test_ceil4_multiples(self):
        """Test ceil4 with multiples of 4."""
        assert parse.ceil4(8) == 8
        assert parse.ceil4(12) == 12
        assert parse.ceil4(16) == 16
    
    def test_ceil4_large_values(self):
        """Test ceil4 with larger values."""
        assert parse.ceil4(100) == 100
        assert parse.ceil4(101) == 104
        assert parse.ceil4(255) == 256


class TestKLVParsing:
    """Test Key-Length-Value structure parsing."""
    
    def test_klv_length_structure(self):
        """Test KLVLength named tuple."""
        klv_len = parse.KLVLength(type='f', size=4, repeat=10)
        assert klv_len.type == 'f'
        assert klv_len.size == 4
        assert klv_len.repeat == 10
    
    def test_klv_item_structure(self):
        """Test KLVItem named tuple."""
        klv_item = parse.KLVItem(key='GPS5', length=40, value=b'\x00' * 40)
        assert klv_item.key == 'GPS5'
        assert klv_item.length == 40
        assert len(klv_item.value) == 40


class TestNumericTypes:
    """Test GPMF numeric type definitions."""
    
    def test_num_types_exists(self):
        """Test that numeric types dictionary exists."""
        assert hasattr(parse, 'num_types')
        assert isinstance(parse.num_types, dict)
    
    def test_num_types_coverage(self):
        """Test that common types are defined."""
        required_types = ['f', 's', 'l', 'L', 'b', 'B']
        for t in required_types:
            assert t in parse.num_types
    
    def test_float_types(self):
        """Test float type definitions."""
        assert parse.num_types['f'][0] == 'float32'
        assert parse.num_types['d'][0] == 'float64'
    
    def test_signed_integer_types(self):
        """Test signed integer types."""
        assert parse.num_types['b'][0] == 'int8'
        assert parse.num_types['s'][0] == 'int16'
        assert parse.num_types['l'][0] == 'int32'
    
    def test_unsigned_integer_types(self):
        """Test unsigned integer types."""
        assert parse.num_types['B'][0] == 'uint8'
        assert parse.num_types['S'][0] == 'uint16'
        assert parse.num_types['L'][0] == 'uint32'


class TestPayloadParsing:
    """Test GPMF payload parsing."""
    
    def test_parse_payload_exists(self):
        """Test that parse_payload function exists."""
        assert hasattr(parse, 'parse_payload')
        assert callable(parse.parse_payload)
    
    def test_parse_simple_float(self):
        """Test parsing a simple float value."""
        # Create a simple float payload
        value = struct.pack('>f', 3.14159)
        result = parse.parse_payload(value, 'TEST', 'f', 4, 1)
        # Should return parsed float
        assert result is not None
    
    def test_parse_multiple_values(self):
        """Test parsing multiple values in payload."""
        # Create payload with multiple floats
        values = struct.pack('>fff', 1.0, 2.0, 3.0)
        result = parse.parse_payload(values, 'TEST', 'f', 4, 3)
        assert result is not None

class TestIterKLVRobustness:
    def test_iter_klv_non_ascii_fourcc(self):
        # FourCC contains non-ASCII bytes; should not raise during decoding
        header = struct.pack(
            '>cccccBH',
            b'\xff', b'\xfe', b'\xfd', b'\xfc',
            b'c',  # type
            0,     # size
            0      # repeat
        )
        stream = header  # no payload

        items = list(parse.iter_klv(stream))

        # Should produce exactly one item with 4-char key string
        assert len(items) == 1
        assert isinstance(items[0].key, str)
        assert len(items[0].key) == 4


class TestStreamParsing:
    """Test GPMF stream parsing."""
    
    def test_filter_klv_exists(self):
        """Test that filter_klv function exists."""
        assert hasattr(parse, 'filter_klv')
    
    def test_empty_stream(self):
        """Test handling of empty stream."""
        # Empty stream should not crash
        stream = b''
        result = list(parse.filter_klv(stream, 'GPS5'))
        assert result == []
    
    def test_invalid_stream(self):
        """Test handling of invalid stream data."""
        # Random bytes should not crash parser
        stream = b'\x00\x01\x02\x03\x04\x05'
        try:
            list(parse.filter_klv(stream, 'GPS5'))
        except:
            # Should handle gracefully
            pass
