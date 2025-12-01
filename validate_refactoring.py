#!/usr/bin/env python3
"""
Simple validation script to test refactoring changes.
This script validates that our new modules can be imported correctly.
"""

import sys
import os

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_constants_module():
    """Test that constants module works correctly."""
    try:
        from pdfCropMargins.constants import (
            DEFAULT_DPI, DEFAULT_X_RESOLUTION, DEFAULT_Y_RESOLUTION,
            DEFAULT_GUI_SCALING_FACTOR, POINTS_PER_INCH
        )
        print("✅ Constants module imported successfully")
        print(f"   DEFAULT_DPI: {DEFAULT_DPI}")
        print(f"   DEFAULT_X_RESOLUTION: {DEFAULT_X_RESOLUTION}")
        print(f"   DEFAULT_Y_RESOLUTION: {DEFAULT_Y_RESOLUTION}")
        print(f"   DEFAULT_GUI_SCALING_FACTOR: {DEFAULT_GUI_SCALING_FACTOR}")
        print(f"   POINTS_PER_INCH: {POINTS_PER_INCH}")
        return True
    except ImportError as e:
        print(f"❌ Failed to import constants: {e}")
        return False

def test_page_configuration_module():
    """Test that PageConfiguration class works correctly."""
    try:
        from pdfCropMargins.page_configuration import PageConfiguration
        
        # Test with None (default values)
        config = PageConfiguration(None)
        print("✅ PageConfiguration class imported successfully")
        print(f"   Default verbose: {config.is_verbose_mode()}")
        print(f"   Default resolution: {config.get_resolution_tuple()}")
        print(f"   Has password: {config.has_password()}")
        
        # Test validation
        warnings = config.validate_settings()
        print(f"   Validation warnings: {len(warnings)}")
        
        return True
    except ImportError as e:
        print(f"❌ Failed to import PageConfiguration: {e}")
        return False

def test_crop_utils_module():
    """Test that crop utilities work correctly."""
    try:
        from pdfCropMargins.crop_utils import (
            calculate_same_size_bounding_box,
            combine_tuple_lists_with_mask,
            validate_crop_arguments
        )
        print("✅ Crop utilities imported successfully")
        
        # Test basic functionality
        test_boxes = [[0, 0, 100, 100], [10, 10, 110, 110], [5, 5, 105, 105]]
        test_pages = {0, 1, 2}
        bbox = calculate_same_size_bounding_box(test_boxes, test_pages, 0)
        print(f"   Sample bounding box calculation: {bbox}")
        
        return True
    except ImportError as e:
        print(f"❌ Failed to import crop utilities: {e}")
        return False

def main():
    """Run validation tests."""
    print("🔍 Validating refactoring changes...")
    print("=" * 50)
    
    tests = [
        test_constants_module,
        test_page_configuration_module, 
        test_crop_utils_module
    ]
    
    results = []
    for test in tests:
        results.append(test())
        print()
    
    print("=" * 50)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"🎉 All {total} tests passed! Refactoring validation successful.")
        return 0
    else:
        print(f"⚠️  {passed}/{total} tests passed. Some issues need attention.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
