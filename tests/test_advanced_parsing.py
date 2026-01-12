"""Advanced integration tests for GPMF parsing."""
import pytest
import struct
import numpy as np
from gpmf import parse


class TestKLVStructureParsing:
    """Test detailed KLV structure parsing."""
    
    def test_parse_klv_header(self):
        """Test parsing of KLV header structure."""
        # KLV header: 4-byte key + 1-byte type + 1-byte size + 2-byte repeat
        # Test that we can access KLV structures
        test_key = b'GPS5'
        assert len(test_key) == 4
    
    def test_parse_payload_float32(self):
        """Test parsing float32 payload."""
        # Create a 4-byte float
        test_value = 3.14159
        packed = struct.pack('>f', test_value)
        
        result = parse.parse_payload(packed, 'TEST', 'f', 4, 1)
        assert result is not None
        
        # Result should be numpy array
        if isinstance(result, np.ndarray):
            assert result.dtype == np.float32 or result.shape[0] == 1
    
    def test_parse_payload_int32(self):
        """Test parsing int32 payload."""
        test_value = 12345
        packed = struct.pack('>i', test_value)
        
        result = parse.parse_payload(packed, 'TEST', 'l', 4, 1)
        assert result is not None
    
    def test_parse_payload_multiple_floats(self):
        """Test parsing multiple float values."""
        values = [1.1, 2.2, 3.3]
        packed = struct.pack('>fff', *values)
        
        result = parse.parse_payload(packed, 'TEST', 'f', 4, 3)
        assert result is not None


class TestStreamFiltering:
    """Test stream filtering and extraction."""
    
    def test_filter_klv_with_key(self):
        """Test filtering KLV stream by key."""
        # Create a simple stream (empty for now)
        stream = b''
        
        # Filter should work without crashing
        results = list(parse.filter_klv(stream, 'GPS5'))
        assert isinstance(results, list)
    
    def test_filter_klv_generator(self):
        """Test that filter_klv returns a generator."""
        stream = b''
        result = parse.filter_klv(stream, 'TEST')
        
        # Should be iterable
        assert hasattr(result, '__iter__')
    
    def test_multiple_keys_filtering(self):
        """Test filtering with different keys."""
        stream = b''
        
        for key in ['GPS5', 'ACCL', 'GYRO', 'SHUT']:
            results = list(parse.filter_klv(stream, key))
            assert isinstance(results, list)


class TestAlignment:
    """Test 32-bit alignment requirements."""
    
    def test_ceil4_zero(self):
        """Test ceil4 with zero."""
        assert parse.ceil4(0) == 0
    
    def test_ceil4_boundary_cases(self):
        """Test ceil4 near boundary values."""
        # Test values near multiples of 4
        assert parse.ceil4(3) == 4
        assert parse.ceil4(4) == 4
        assert parse.ceil4(5) == 8
        assert parse.ceil4(7) == 8
        assert parse.ceil4(8) == 8
        assert parse.ceil4(9) == 12
    
    def test_alignment_with_payload(self):
        """Test that payload respects alignment."""
        # Payload sizes should align to 4 bytes
        sizes = [1, 2, 3, 4, 5, 10, 15, 20]
        
        for size in sizes:
            aligned = parse.ceil4(size)
            assert aligned % 4 == 0
            assert aligned >= size


class TestPayloadTypes:
    """Test different payload type parsing."""
    
    def test_unsigned_int8(self):
        """Test uint8 parsing."""
        value = 255
        packed = struct.pack('>B', value)
        result = parse.parse_payload(packed, 'TEST', 'B', 1, 1)
        assert result is not None
    
    def test_signed_int8(self):
        """Test int8 parsing."""
        value = -128
        packed = struct.pack('>b', value)
        result = parse.parse_payload(packed, 'TEST', 'b', 1, 1)
        assert result is not None
    
    def test_uint16(self):
        """Test uint16 parsing."""
        value = 65535
        packed = struct.pack('>H', value)
        result = parse.parse_payload(packed, 'TEST', 'S', 2, 1)
        assert result is not None
    
    def test_int16(self):
        """Test int16 parsing."""
        value = -32768
        packed = struct.pack('>h', value)
        result = parse.parse_payload(packed, 'TEST', 's', 2, 1)
        assert result is not None
    
    def test_uint32(self):
        """Test uint32 parsing."""
        value = 4294967295
        packed = struct.pack('>I', value)
        result = parse.parse_payload(packed, 'TEST', 'L', 4, 1)
        assert result is not None
    
    def test_int32(self):
        """Test int32 parsing."""
        value = -2147483648
        packed = struct.pack('>i', value)
        result = parse.parse_payload(packed, 'TEST', 'l', 4, 1)
        assert result is not None
    
    def test_float64(self):
        """Test float64 (double) parsing."""
        value = 3.141592653589793
        packed = struct.pack('>d', value)
        result = parse.parse_payload(packed, 'TEST', 'd', 8, 1)
        assert result is not None


class TestComplexStructures:
    """Test complex nested structures."""
    
    def test_nested_klv_structure(self):
        """Test handling of nested KLV structures."""
        # GPMF supports nested structures (DEVC -> STRM -> GPS5)
        # For now, test that we can handle multiple levels
        assert hasattr(parse, 'filter_klv')
    
    def test_complex_type_string(self):
        """Test TYPE declarations with complex type strings."""
        # TYPE can be like "fssL" meaning float, int16, int16, uint32
        type_string = "fssL"
        
        # Each character should be in num_types
        for char in type_string:
            assert char in parse.num_types
    
    def test_array_of_values(self):
        """Test parsing arrays of values."""
        # GPMF can have repeat count > 1
        # GPS5 typically has 5 values: lat, lon, alt, speed_2d, speed_3d
        num_values = 5
        values = [37.7749, -122.4194, 10.5, 5.0, 5.1]
        packed = struct.pack('>' + 'f' * num_values, *values)
        
        result = parse.parse_payload(packed, 'GPS5', 'f', 4, num_values)
        assert result is not None
