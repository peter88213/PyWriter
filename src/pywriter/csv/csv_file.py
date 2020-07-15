"""CsvFile - Class for csv file generation.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.file.file_export import FileExport


class CsvFile(FileExport):
    """csv file representation.
    * Records are separated by line breaks.
    * Data fields are delimited by the _SEPARATOR character.
    """

    EXTENSION = '.csv'
    # overwrites Novel._FILE_EXTENSION

    _SEPARATOR = '|'     # delimits data fields within a record.
    _LINEBREAK = '\t'    # substitutes embedded line breaks.

    def convert_markup(self, text):
        """Convert yw7 raw markup to odt. Return an xml string."""

        try:
            text = text.rstrip().replace('\n', self._LINEBREAK)

        except AttributeError:
            text = ''

        return text

    def get_structure(self):
        """This file format has no comparable structure."""
        return None
