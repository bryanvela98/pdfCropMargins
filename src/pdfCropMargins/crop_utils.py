"""
Extracted methods from the complex calculate_crop_list function.

This module contains smaller, more focused methods that were extracted
from the original 400+ line calculate_crop_list method to improve 
maintainability and readability.
"""

from .constants import DEFAULT_PERCENT_RETAIN


def calculate_same_size_bounding_box(full_page_box_list, page_nums_to_crop, order_n=0):
    """
    Calculate a bounding box that encompasses all selected pages.
    
    Args:
        full_page_box_list: List of page bounding boxes
        page_nums_to_crop: Set of page numbers to include in calculation
        order_n: Order statistic to apply (ignore n largest margins)
        
    Returns:
        list: [left, bottom, right, top] coordinates of the bounding box
    """
    same_size_bounding_box = [
        # We want the smallest of the left and bottom edges.
        sorted(full_page_box_list[pg][0] for pg in page_nums_to_crop),
        sorted(full_page_box_list[pg][1] for pg in page_nums_to_crop),
        # We want the largest of the right and top edges.
        sorted((full_page_box_list[pg][2] for pg in page_nums_to_crop), reverse=True),
        sorted((full_page_box_list[pg][3] for pg in page_nums_to_crop), reverse=True)
    ]
    return [sortlist[order_n] for sortlist in same_size_bounding_box]


def combine_tuple_lists_with_mask(mask, default_list, optional_list):
    """
    Combine two lists of tuples using a mask.
    
    A utility function used for processing options like 'samePageSize4'.
    The mask is a four-tuple of strings 't' or 'f' for replacing elements 
    of `default_list` with the corresponding elements of `optional_list`.
    
    Args:
        mask: Four-character string of 't' or 'f'
        default_list: List of default tuples
        optional_list: List of optional tuples to use when mask is 't'
        
    Returns:
        list: Combined list of tuples
    """
    final_list = []
    for default_tuple, optional_tuple in zip(default_list, optional_list):
        new_default_tuple = list(default_tuple)
        for index, char in enumerate(mask):
            if char == "t":
                new_default_tuple[index] = optional_tuple[index]
        final_list.append(tuple(new_default_tuple))
    return final_list


def handle_same_page_size_option(args, full_page_box_list, page_nums_to_crop, num_pages_to_crop):
    """
    Handle the '--samePageSize' and '--setSamePageSize' options.
    
    Extract method: This was originally part of calculate_crop_list but was
    extracted to reduce complexity and improve readability.
    
    Args:
        args: Command line arguments
        full_page_box_list: List of page bounding boxes
        page_nums_to_crop: Set of page numbers to crop
        num_pages_to_crop: Number of pages to crop
        
    Returns:
        list: Modified full_page_box_list with same-size adjustments
    """
    # Handle order statistic option
    order_n = 0
    if args.samePageSizeOrderStat:
        args.samePageSize = True
        order_n = min(args.samePageSizeOrderStat[0], num_pages_to_crop - 1)
        order_n = max(order_n, 0)

    if not (args.samePageSize or args.setSamePageSize):
        return full_page_box_list

    if args.samePageSize:  
        # Calculate the page containing all the other selected pages
        if args.verbose:
            print("\nSetting each page size to the smallest box bounding all the pages.")
            if order_n != 0:
                print("But ignoring the largest {} pages in calculating each edge."
                      .format(order_n))
        
        same_size_bounding_box = calculate_same_size_bounding_box(
            full_page_box_list, page_nums_to_crop, order_n)
    else:  
        # Set the page size to the box passed in (ignored if `--samePageSize` is set)
        same_size_bounding_box = [float(f) for f in args.setSamePageSize]
        if args.verbose:
            print("\nSetting each page size to the bounding box passed in:"
                  f"\n   {same_size_bounding_box}")

    num_pages = len(full_page_box_list)
    same_size_bounding_box_list = [same_size_bounding_box] * num_pages

    if args.samePageSize4:
        same_size_bounding_box_list = combine_tuple_lists_with_mask(
            args.samePageSize4, full_page_box_list, same_size_bounding_box_list)

    # Set `full_page_box_list` to `same_size_bounding_box` for the pages selected
    new_full_page_box_list = []
    for p_num, f_box in enumerate(full_page_box_list):
        if p_num not in page_nums_to_crop:
            new_full_page_box_list.append(f_box)
        else:
            new_full_page_box_list.append(same_size_bounding_box_list[p_num])
    
    return new_full_page_box_list


def validate_crop_arguments(args):
    """
    Validate and normalize crop-related command line arguments.
    
    Extract method: This logic was originally scattered throughout 
    calculate_crop_list but was extracted for clarity.
    
    Args:
        args: Command line arguments object
        
    Returns:
        dict: Normalized argument values with validation applied
    """
    # Validate and set default percent retain values
    if not args.percentRetain4:
        percent_retain_4 = [args.percentRetain[0]] * 4
    else:
        percent_retain_4 = args.percentRetain4.copy()
        
    # Validate and set default absolute offset values  
    if not args.absoluteOffset4:
        absolute_offset_4 = [args.absoluteOffset[0]] * 4
    else:
        absolute_offset_4 = args.absoluteOffset4.copy()
        
    # Validate and set default uniform order stat values
    if not args.uniformOrderStat4:
        uniform_order_stat_4 = [args.uniformOrderStat[0]] * 4 if args.uniformOrderStat else [0] * 4
    else:
        uniform_order_stat_4 = args.uniformOrderStat4.copy()
        
    return {
        'percent_retain_4': percent_retain_4,
        'absolute_offset_4': absolute_offset_4,
        'uniform_order_stat_4': uniform_order_stat_4
    }
