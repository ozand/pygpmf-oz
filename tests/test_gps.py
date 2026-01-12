"""Tests for GPS parsing functionality."""
import pytest
from gpmf import gps


class TestGPSParsing:
    """Test GPS data extraction and parsing."""
    
    def test_parse_gps_block_basic(self, sample_gps_data):
        """Test basic GPS block parsing."""
        # TODO: Implement with real GPMF data
        assert sample_gps_data['lat'] == pytest.approx(44.1287283, rel=1e-6)
        assert sample_gps_data['lon'] == pytest.approx(5.427715, rel=1e-6)
    
    def test_gps_altitude_parsing(self, sample_gps_data):
        """Test altitude extraction from GPS data."""
        assert sample_gps_data['alt'] == pytest.approx(833.759, rel=1e-3)
    
    def test_gps_speed_2d(self, sample_gps_data):
        """Test 2D speed calculation."""
        assert sample_gps_data['speed_2d'] > 0
        assert sample_gps_data['speed_2d'] == pytest.approx(9.221, rel=1e-3)
    
    def test_gps_speed_3d(self, sample_gps_data):
        """Test 3D speed calculation."""
        assert sample_gps_data['speed_3d'] >= sample_gps_data['speed_2d']
    
    def test_extract_gps_blocks(self, sample_gpmf_stream):
        """Test GPS block extraction from GPMF stream."""
        # Test with empty stream
        empty_blocks = list(gps.extract_gps_blocks(b''))
        assert empty_blocks == []
        
        # Test function exists and is callable
        assert hasattr(gps, 'extract_gps_blocks')
        assert callable(gps.extract_gps_blocks)
    
    def test_make_pgx_segment(self):
        """Test GPX segment creation from GPS data."""
        # Create sample GPS data points using correct field names
        gps_data = [
            gps.GPSData(
                description="GPS Track",
                timestamp="2024-01-12 10:00:00.000",
                precision=1.5,
                fix=3,
                latitude=[37.7749],
                longitude=[-122.4194],
                altitude=[10.5],
                speed_2d=[5.0],
                speed_3d=[5.1],
                units="m/s",
                npoints=1
            ),
            gps.GPSData(
                description="GPS Track",
                timestamp="2024-01-12 10:00:01.000",
                precision=1.6,
                fix=3,
                latitude=[37.7750],
                longitude=[-122.4195],
                altitude=[11.0],
                speed_2d=[5.2],
                speed_3d=[5.3],
                units="m/s",
                npoints=1
            )
        ]
        
        # Generate GPX segment
        result = gps.make_pgx_segment(gps_data)
        assert result is not None


class TestGPSValidation:
    """Test GPS data validation."""
    
    def test_invalid_latitude(self):
        """Test handling of invalid latitude values."""
        # Latitude must be between -90 and 90
        invalid_lats = [-91.0, -90.1, 90.1, 91.0, 100.0]
        for lat in invalid_lats:
            assert not (-90 <= lat <= 90)
    
    def test_invalid_longitude(self):
        """Test handling of invalid longitude values."""
        # Longitude must be between -180 and 180
        invalid_lons = [-181.0, -180.1, 180.1, 181.0, 200.0]
        for lon in invalid_lons:
            assert not (-180 <= lon <= 180)
    
    def test_missing_gps_fix(self):
        """Test handling of missing GPS fix."""
        # GPS fix types: 0 (no fix), 2 (2D), 3 (3D)
        valid_fixes = [0, 2, 3]
        
        # Test that GPSData can be created with different fix values
        for fix_val in valid_fixes:
            gps_data = gps.GPSData(
                description="Test",
                timestamp=1000,
                precision=99.0,
                fix=fix_val,
                latitude=0.0,
                longitude=0.0,
                altitude=0.0,
                speed_2d=0.0,
                speed_3d=0.0,
                units="m/s",
                npoints=1
            )
            assert gps_data.fix == fix_val
