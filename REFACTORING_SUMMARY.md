## Code Smells Addressed

### 1. Magic Numbers 

**Issue**: Hardcoded values scattered throughout the codebase (0.90 scaling factors, 72 DPI defaults, etc.)

**Solution**: **Introduce Explaining Variable (Set I)**

- Created `constants.py` module with named constants
- Replaced magic numbers in `manpage_data.py` and `external_program_calls.py`
- Fixed inconsistency where default was 72 but help text said 150

### 2. Complex Methods 

**Issue**: `calculate_crop_list` method was 435+ lines long, violating single responsibility principle

**Solution**: **Extract Method (Set I)**

- Created `crop_utils.py` module
- Extracted `handle_same_page_size_option()` method (reduced ~40 lines)
- Extracted `calculate_same_size_bounding_box()` utility method
- Extracted `combine_tuple_lists_with_mask()` utility method
- Extracted `validate_crop_arguments()` method

### 3. Feature Envy

**Issue**: `MuPdfDocument` class was obsessed with `args` object, accessing it extensively

**Solution**: **Extract Class (Set II)** + **Move Method (Set II)**

- Created `PageConfiguration` class to encapsulate page-related settings
- Moved args-related logic to dedicated configuration object
- Refactored MuPdfDocument constructor to use PageConfiguration
- Added methods like `has_password()`, `get_password()`, `get_resolution_tuple()`

### 4. Deficient Encapsulation (Medium)

**Issue**: Global `args` variable used across modules

**Solution**: **Move Method (Set II)** - Partial implementation

- Started encapsulation through PageConfiguration class
- Reduced direct args access in MuPdfDocument methods

## Refactoring Techniques Applied

### Set I Techniques

1. **✅ Extract Method**: Broke down complex `calculate_crop_list` method
2. **✅ Introduce Explaining Variable**: Created constants for magic numbers
3. **✅ Rename Method/Variable**: Improved method names in extracted utilities
4. **✅ Decompose Conditional**: Simplified complex conditional logic in extracted methods

### Set II Techniques

1. **✅ Extract Class**: Created `PageConfiguration` class
2. **✅ Move Method**: Moved args-related functionality to PageConfiguration
3. **✅ Move Field**: Moved configuration data to PageConfiguration

## Files Created/Modified

### New Files Created:

1. **`constants.py`** - Centralized magic number definitions
2. **`page_configuration.py`** - PageConfiguration class for encapsulating page settings
3. **`crop_utils.py`** - Extracted utility methods for crop calculations

### Files Modified:

1. **`manpage_data.py`** - Updated to use constants instead of magic numbers
2. **`external_program_calls.py`** - Updated function signatures to use constants
3. **`main_pdfCropMargins.py`** - Refactored to use extracted methods
4. **`pymupdf_routines.py`** - Refactored to use PageConfiguration

## Code Quality Improvements

### Before Refactoring:

- `calculate_crop_list`: 435+ lines (extremely complex)
- Magic numbers scattered throughout codebase
- MuPdfDocument heavily coupled to args object
- Global args variable creating tight coupling

### After Refactoring:

- `calculate_crop_list`: Reduced by ~40+ lines with extracted methods
- Magic numbers replaced with named constants
- MuPdfDocument uses PageConfiguration for cleaner separation
- Improved encapsulation and reduced coupling

## Technical Benefits

1. **Improved Maintainability**: Smaller, focused methods are easier to understand and modify
2. **Better Testability**: Extracted methods can be tested independently
3. **Reduced Coupling**: PageConfiguration reduces dependencies between classes
4. **Enhanced Readability**: Named constants make code self-documenting
5. **Consistency**: Fixed inconsistencies between defaults and documentation

## Example Improvements

### Magic Numbers → Constants

```python
# Before
cmd_parser.add_argument("-x", "--resX", type=int, default=72)
resolution = self.args.resX, self.args.resY

# After
from .constants import DEFAULT_DPI
cmd_parser.add_argument("-x", "--resX", type=int, default=DEFAULT_DPI)
resolution = self.page_config.get_resolution_tuple()
```

### Complex Method → Extracted Methods

```python
# Before: 435+ line calculate_crop_list method with inline logic

# After: Clean delegation to extracted methods
full_page_box_list = handle_same_page_size_option(
    args, full_page_box_list, page_nums_to_crop, num_pages_to_crop)
```

### Feature Envy → Proper Encapsulation

```python
# Before
if self.args.password:
    authenticate_code = self.document.authenticate(self.args.password)

# After
if self.page_config.has_password():
    authenticate_code = self.document.authenticate(self.page_config.get_password())
```
