"""Helper module to set a custom icon at the tk windows.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import sys
import tkinter as tk


def set_icon(widget, icon='logo', path=None):
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
    if path is None:
        path = os.path.dirname(sys.argv[0])
        if not path:
            path = '.'
        path = f'{path}/icons'
    if os.name == 'nt':
        try:
            widget.iconbitmap(default=f'{path}/{icon}.ico')
        except:
            return False
    else:
        try:
            pic = tk.PhotoImage(file=f'{path}/{icon}.png')
            widget.iconphoto(False, pic)
        except:
            return False

    return True

