"""
Constants for pdfCropMargins program.

This module contains all the magic numbers and configuration constants
used throughout the program to improve maintainability and readability.
"""

# Default resolution values
DEFAULT_DPI = 72
DEFAULT_X_RESOLUTION = 150
DEFAULT_Y_RESOLUTION = 150

# GUI scaling and sizing constants
DEFAULT_GUI_SCALING_FACTOR = 0.90
WINDOW_SIZE_SCALING_FACTOR = 0.90
GUI_FONT_SIZE_DEFAULT = 10

# PDF coordinate system constants
POINTS_PER_INCH = 72

# Decimal precision for PDF values
DECIMAL_PRECISION_FOR_MARGIN_POINT_VALUES = 8

# Default percentage values
DEFAULT_PERCENT_RETAIN = 10.0
DEFAULT_MARGIN_PERCENTAGE = 0.0

# Producer metadata strings
PRODUCER_MODIFIER = " (Cropped by pdfCropMargins.)"
PRODUCER_MODIFIER_2 = " (Cropped by pdfCropMargins>=2.0.)"
RESTORE_METADATA_KEY = "pdfCropMarginsRestoreData"

# File naming defaults
DEFAULT_CROPPED_SUFFIX = "_cropped"
DEFAULT_UNCROPPED_SUFFIX = "_uncropped"
DEFAULT_STRING_SEPARATOR = ""

# Box type constants
MEDIABOX = "mediabox"
CROPBOX = "cropbox"
TRIMBOX = "trimbox"
ARTBOX = "artbox"
BLEEDBOX = "bleedbox"

# Rotation angle constants
ROTATION_0_DEGREES = 0
ROTATION_90_DEGREES = 90
ROTATION_180_DEGREES = 180
ROTATION_270_DEGREES = 270
VALID_ROTATION_ANGLES = [ROTATION_0_DEGREES, ROTATION_90_DEGREES, 
                        ROTATION_180_DEGREES, ROTATION_270_DEGREES]

# Page ratio weights default
DEFAULT_PAGE_RATIO_WEIGHTS = [1.0, 1.0, 1.0, 1.0]

# Memory and performance constants
MAX_IMAGE_SIZE_THRESHOLD = 60000  # 60KB for output truncation
TEMP_DIR_PREFIX = "pdfCropMargins_"
