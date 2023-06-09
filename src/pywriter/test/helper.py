"""Helper module for reading utf-8 or ANSI encoded files.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""


def read_file(inputFile):
    """Read a utf-8 or ANSI encoded text file.
    
    Positional arguments:
        inputFile -- str: path of the file to read.
        
    Return a string.
    """
    try:
        with open(inputFile, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        # HTML files exported by a word processor may be ANSI encoded.
        with open(inputFile, 'r') as f:
            return f.read()
