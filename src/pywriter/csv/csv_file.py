"""Provide a generic class for csv file import.

Other csv file representations inherit from this class.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import csv

from pywriter.model.novel import Novel


class CsvFile(Novel):
    """csv file representation.

    - Records are separated by line breaks.
    - Data fields are delimited by the _SEPARATOR character.
    """

    EXTENSION = '.csv'
    # overwrites Novel.EXTENSION

    _SEPARATOR = ','
    # delimits data fields within a record.

    rowTitles = []

    def read(self):
        """Parse the csv file located at filePath, fetching the rows.
        Check the number of fields in each row.
        Return a message beginning with SUCCESS or ERROR.
        Override the superclass method.
        """
        self.rows = []
        cellsPerRow = len(self.rowTitles)

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
            return 'ERROR: "{}" not found.'.format(os.path.normpath(self.filePath))

        except:
            return 'ERROR: Can not parse "{}".'.format(os.path.normpath(self.filePath))

        return 'SUCCESS'

    def get_list(self, text):
        """Split a sequence of comma separated strings into a list of strings.
        Remove leading and trailing spaces, if any.
        """
        elements = []
        tempList = text.split(',')

        for element in tempList:
            elements.append(element.strip())

        return elements
