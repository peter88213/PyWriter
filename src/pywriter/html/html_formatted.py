"""Provide a base class for HTML documents containing text that is formatted in yWriter.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.html.html_file import HtmlFile


class HtmlFormatted(HtmlFile):
    """HTML file representation.

    Provide methods and data for processing chapters with formatted text.
    """
    _COMMENT_START = '/*'
    _COMMENT_END = '*/'
    _SC_TITLE_BRACKET = '~'
    _BULLET = '-'
    _INDENT = '>'

    def __init__(self, filePath, **kwargs):
        """Add instance variables.

        Extends the superclass constructor.
        """
        super().__init__(filePath)
        self.languages = []

    def _cleanup_scene(self, text):
        """Clean up yWriter markup.
        
        Positional arguments:
            text -- string to clean up.
        
        Return a yw7 markup string.
        """
        #--- Remove orphaned tags.
        text = text.replace('[/b][b]', '')
        text = text.replace('[/i][i]', '')
        text = text.replace('[/b][b]', '')

        #--- Remove misplaced formatting tags.
        # text = re.sub('\[\/*[b|i]\]', '', text)
        return text

