"""Provide a class for ODT invisibly tagged "Notes" chapters import.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.pywriter_globals import *
from pywriter.html.html_manuscript import HtmlManuscript


class HtmlNotes(HtmlManuscript):
    """ODT "Notes" chapters file reader.

    Import a manuscript with invisibly tagged chapters and scenes.
    """
    DESCRIPTION = _('Notes chapters')
    SUFFIX = '_notes'

    _TYPE = 1
