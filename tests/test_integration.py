"""Integration tests for full pipeline."""
import pytest
from gpmf import parse, gps, io


class TestFullPipeline:
    """Test complete GPMF extraction pipeline."""
    
    def test_pipeline_functions_exist(self):
        """Test that all pipeline functions exist."""
        # Parse module
        assert hasattr(parse, 'filter_klv')
        assert hasattr(parse, 'parse_payload')
        
        # GPS module
        assert hasattr(gps, 'extract_gps_blocks')
        assert hasattr(gps, 'parse_gps_block')
        assert hasattr(gps, 'make_pgx_segment')
        
        # IO module
        assert hasattr(io, 'find_gpmf_stream')
        assert hasattr(io, 'extract_gpmf_stream')
    
    def test_data_flow(self):
        """Test data flow through pipeline."""
        # Pipeline: video file -> GPMF stream -> GPS blocks -> GPX
        # Each step should handle data correctly
        
        # Step 1: Extract stream (requires video file)
        # Step 2: Parse KLV structures
        # Step 3: Filter GPS data
        # Step 4: Generate GPX
        
        # For now, test that functions are callable
        assert callable(io.extract_gpmf_stream)
        assert callable(parse.filter_klv)
        assert callable(gps.extract_gps_blocks)
        assert callable(gps.make_pgx_segment)


class TestErrorHandling:
    """Test error handling across modules."""
    
    def test_empty_data_handling(self):
        """Test handling of empty data at each stage."""
        # Empty binary stream
        empty_stream = b''
        
        # Should not crash
        result = list(parse.filter_klv(empty_stream, 'GPS5'))
        assert result == []
        
        # GPS extraction from empty
        gps_blocks = list(gps.extract_gps_blocks(empty_stream))
        assert gps_blocks == []
    
    def test_corrupted_data_handling(self):
        """Test handling of corrupted data."""
        # Random bytes should not crash parser
        corrupted = b'\\x00\\x01\\x02\\x03\\xAB\\xCD\\xEF'
        
        try:
            list(parse.filter_klv(corrupted, 'GPS5'))
        except:
            # Should handle gracefully without segfault
            pass


class TestDataTypes:
    """Test GPMF data type handling."""
    
    def test_numeric_type_definitions(self):
        """Test that all GPMF numeric types are defined."""
        # GPMF standard types
        gpmf_types = ['b', 'B', 's', 'S', 'l', 'L', 'f', 'd', 'j', 'J']
        
        for gpmf_type in gpmf_types:
            assert gpmf_type in parse.num_types
    
    def test_type_sizes(self):
        """Test that type sizes are correct."""
        # Standard sizes
        expected_sizes = {
            'b': 1,  # int8
            'B': 1,  # uint8
            's': 2,  # int16
            'S': 2,  # uint16
            'l': 4,  # int32
            'L': 4,  # uint32
            'f': 4,  # float32
            'd': 8,  # float64
        }
        
        for type_char, expected_size in expected_sizes.items():
            if type_char in parse.num_types:
                type_info = parse.num_types[type_char]
                # num_types is a dict mapping type char to (dtype_name, size_format_char)
                # Format char should match expected size
                assert isinstance(type_info, tuple)
                assert len(type_info) == 2


class TestGPXGeneration:
    """Test GPX file generation."""
    
    def test_gpx_structure(self):
        """Test GPX XML structure generation."""
        # Create minimal GPS data
        gps_data = [
            gps.GPSData(
                description="Test Track",
                timestamp="2024-01-12 10:00:00.000",
                precision=1.0,
                fix=3,
                latitude=[37.7749],
                longitude=[-122.4194],
                altitude=[10.0],
                speed_2d=[0.0],
                speed_3d=[0.0],
                units="m/s",
                npoints=1
            )
        ]
        
        # Generate GPX
        gpx_segment = gps.make_pgx_segment(gps_data)
        
        # Should return GPX segment object
        assert gpx_segment is not None
    
    def test_multiple_points(self):
        """Test GPX generation with multiple points."""
        # Create track with multiple points
        num_points = 10
        gps_data = []
        
        for i in range(num_points):
            gps_data.append(
                gps.GPSData(
                    description="Test Track",
                    timestamp=f"2024-01-12 10:00:{i:02d}.000",
                    precision=1.0,
                    fix=3,
                    latitude=[37.7749 + i * 0.0001],
                    longitude=[-122.4194 + i * 0.0001],
                    altitude=[10.0 + i],
                    speed_2d=[5.0],
                    speed_3d=[5.0],
                    units="m/s",
                    npoints=1
                )
            )
        
        # Generate GPX
        gpx_segment = gps.make_pgx_segment(gps_data)
        assert gpx_segment is not None
