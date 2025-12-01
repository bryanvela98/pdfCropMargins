"""
Page configuration and settings management for pdfCropMargins.

This module contains the PageConfiguration class that encapsulates
page-related settings and reduces feature envy in the MuPdfDocument class.
"""

from .constants import (
    DEFAULT_DPI, DEFAULT_X_RESOLUTION, DEFAULT_Y_RESOLUTION,
    DEFAULT_PERCENT_RETAIN, DECIMAL_PRECISION_FOR_MARGIN_POINT_VALUES,
    VALID_ROTATION_ANGLES, DEFAULT_PAGE_RATIO_WEIGHTS
)


class PageConfiguration:
    """
    Encapsulates page-related configuration settings to reduce coupling
    between document processing classes and command-line arguments.
    
    This class addresses the Feature Envy code smell by consolidating
    page-related settings that were previously scattered across multiple
    classes.
    """
    
    def __init__(self, args=None):
        """
        Initialize page configuration from command-line arguments.
        
        Args:
            args: Parsed command-line arguments object from argparse
        """
        if args is None:
            self._set_default_values()
        else:
            self._set_values_from_args(args)
    
    def _set_default_values(self):
        """Set default configuration values."""
        self.verbose = False
        self.password = None
        self.res_x = DEFAULT_DPI
        self.res_y = DEFAULT_DPI
        self.full_page_box = ["m", "c"]  # MediaBox and CropBox intersection
        self.absolute_precrop_4 = [0.0, 0.0, 0.0, 0.0]
        self.percent_retain = DEFAULT_PERCENT_RETAIN
        self.percent_retain_4 = [DEFAULT_PERCENT_RETAIN] * 4
        self.write_crop_data_to_file = None
        self.boxes_to_set = ["m"]  # MediaBox by default
        self.page_ratio_weights = DEFAULT_PAGE_RATIO_WEIGHTS.copy()
        
    def _set_values_from_args(self, args):
        """Set values from command-line arguments object."""
        self.verbose = getattr(args, 'verbose', False)
        self.password = getattr(args, 'password', None)
        self.res_x = getattr(args, 'resX', DEFAULT_DPI)
        self.res_y = getattr(args, 'resY', DEFAULT_DPI)
        self.full_page_box = getattr(args, 'fullPageBox', ["m", "c"])
        self.absolute_precrop_4 = getattr(args, 'absolutePreCrop4', [0.0, 0.0, 0.0, 0.0])
        self.percent_retain = getattr(args, 'percentRetain', [DEFAULT_PERCENT_RETAIN])[0]
        self.percent_retain_4 = getattr(args, 'percentRetain4', [DEFAULT_PERCENT_RETAIN] * 4)
        self.write_crop_data_to_file = getattr(args, 'writeCropDataToFile', None)
        self.boxes_to_set = getattr(args, 'boxesToSet', ["m"])
        self.page_ratio_weights = getattr(args, 'pageRatioWeights', DEFAULT_PAGE_RATIO_WEIGHTS.copy())
    
    def get_resolution_tuple(self):
        """
        Get the resolution as a tuple for rendering operations.
        
        Returns:
            tuple: (res_x, res_y) resolution values
        """
        return (self.res_x, self.res_y)
    
    def is_verbose_mode(self):
        """
        Check if verbose output is enabled.
        
        Returns:
            bool: True if verbose mode is enabled
        """
        return self.verbose
    
    def has_password(self):
        """
        Check if a password is provided for encrypted documents.
        
        Returns:
            bool: True if password is provided
        """
        return self.password is not None
    
    def get_password(self):
        """
        Get the password for encrypted documents.
        
        Returns:
            str or None: The password string or None
        """
        return self.password
    
    def should_write_crop_data(self):
        """
        Check if crop data should be written to a file.
        
        Returns:
            bool: True if crop data should be written
        """
        return self.write_crop_data_to_file is not None
    
    def get_crop_data_filename(self):
        """
        Get the filename for writing crop data.
        
        Returns:
            str or None: The filename or None
        """
        return self.write_crop_data_to_file
    
    def validate_settings(self):
        """
        Validate configuration settings and fix any inconsistencies.
        
        Returns:
            list: List of warning messages about fixes applied
        """
        warnings = []
        
        # Ensure resolution values are positive
        if self.res_x <= 0:
            self.res_x = DEFAULT_DPI
            warnings.append(f"Invalid X resolution, reset to {DEFAULT_DPI}")
            
        if self.res_y <= 0:
            self.res_y = DEFAULT_DPI
            warnings.append(f"Invalid Y resolution, reset to {DEFAULT_DPI}")
        
        # Validate percent retain values
        if not isinstance(self.percent_retain_4, list) or len(self.percent_retain_4) != 4:
            self.percent_retain_4 = [self.percent_retain] * 4
            warnings.append("Fixed percent_retain_4 to have 4 values")
            
        # Validate absolute precrop values
        if not isinstance(self.absolute_precrop_4, list) or len(self.absolute_precrop_4) != 4:
            self.absolute_precrop_4 = [0.0, 0.0, 0.0, 0.0]
            warnings.append("Fixed absolute_precrop_4 to have 4 values")
        
        return warnings
    
    def __repr__(self):
        """String representation for debugging."""
        return (f"PageConfiguration(verbose={self.verbose}, "
                f"resolution={self.res_x}x{self.res_y}, "
                f"boxes={self.full_page_box})")
