"""Provide a class for html invisibly tagged "Todo" chapters import.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.pywriter_globals import *
from pywriter.html.html_manuscript import HtmlManuscript


class HtmlTodo(HtmlManuscript):
    """HTML "Todo" chapters file representation.

    Import a manuscript with invisibly tagged chapters and scenes.
    """
    DESCRIPTION = _('Todo chapters')
    SUFFIX = '_todo'

    _TYPE = 2
