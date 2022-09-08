"""Helper module to set a custom icon at the tk windows.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import sys


def set_icon(widget, icon='logo', path=f'{os.path.dirname(sys.argv[0])}/icons/'):
    """Set the window icon to the "widget" window and all its children.
    
    Positional arguments:
        widget -- tk object: The tk application window.
        
    Optional arguments:
        icon -- str: The icon filename without extension.
        path -- str: The directory containing the icons.
    
    Under Windows, the "ico" filetype is required, 
    otherwise the "png" image is used.
    
    Return False, if an error occurs, otherwise return True.
    """
    if os.name == 'nt':
        extension = '.ico'
    else:
        extension = '.png'
    try:
        widget.iconbitmap(default=f'{path}{icon}{extension}')
    except:
        return False

    return True

