"""CsvFile - Class for csv file generation.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import csv

from pywriter.file.file_export import FileExport


class CsvFile(FileExport):
    """csv file representation.
    * Records are separated by line breaks.
    * Data fields are delimited by the _SEPARATOR character.
    """

    EXTENSION = '.csv'
    # overwrites Novel.EXTENSION

    _SEPARATOR = '|'
    # delimits data fields within a record.

    CSV_REPLACEMENTS = []

    def convert_from_yw(self, text):
        """Convert line breaks."""

        try:
            text = text.rstrip()

            for r in self.CSV_REPLACEMENTS:
                text = text.replace(r[0], r[1])

        except AttributeError:
            text = ''

        return text

    def convert_to_yw(self, text):
        """Convert line breaks."""

        try:

            for r in self.CSV_REPLACEMENTS:
                text = text.replace(r[1], r[0])

        except AttributeError:
            text = ''

        return text

    def read(self):
        """Parse the csv file located at filePath, fetching the rows.
        Check the number of fields in each row.
        Return a message beginning with SUCCESS or ERROR.
        """
        self.rows = []
        cellsPerRow = len(self.fileHeader.split(self._SEPARATOR))

        try:
            with open(self.filePath, newline='', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=self._SEPARATOR)

                for row in reader:
                    # Each row read from the csv file is returned
                    # as a list of strings

                    if len(row) != cellsPerRow:
                        return 'ERROR: Wrong csv structure.'

                    self.rows.append(row)

        except(FileNotFoundError):
            return 'ERROR: "' + os.path.normpath(self.filePath) + '" not found.'

        except:
            return 'ERROR: Can not parse "' + os.path.normpath(self.filePath) + '".'

        return 'SUCCESS'
