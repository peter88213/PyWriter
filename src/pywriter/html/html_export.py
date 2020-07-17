"""HtmlExport - Class for html export with templates.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.file.file_export import FileExport


class HtmlExport(FileExport):
    EXTENSION = '.html'
    # overwrites Novel._FILE_EXTENSION

    def convert_from_yw(self, text):
        """Convert yw7 markup to target format."""

        try:
            text = text.replace('\n', '</p>\n<p>')
            text = text.replace('[i]', '<em>')
            text = text.replace('[/i]', '</em>')
            text = text.replace('[b]', '<strong>')
            text = text.replace('[/b]', '</strong>')
            text = text.replace('<p></p>', '<p><br /></p>')
            text = text.replace('/*', '<!--')
            text = text.replace('*/', '-->')

        except AttributeError:
            text = ''

        return(text)
