"""Provide a class for parsing ODS documents.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys
from io import StringIO
import zipfile
import xml.etree.ElementTree as ET
from pywriter.pywriter_globals import *


class OdsParser():
    """An ODS document parser.
    
    Public methods:
        get_rows(filePath, cellsPerRow) -- Return rows and cells from an ODS document.
           
    Return a list of rows, containing lists of column cells.
    The PyWriter csv import classes thus can be reused.
    """

    def __init__(self):
        super().__init__()
        self._rows = []
        self._cells = []
        self._inCell = None
        self.__cellsPerRow = 0

    def get_rows(self, filePath, cellsPerRow):
        """Return a nested list with rows and cells from an ODS document.
        
        Positional arguments:
            filePath -- str: ODS document path.
            cellsPerRow -- int: Number of cells per row.
        
        First unzip the ODS file located at self.filePath, then parse content.xml.
        """
        ns = dict(
            office='urn:oasis:names:tc:opendocument:xmlns:office:1.0',
            text='urn:oasis:names:tc:opendocument:xmlns:text:1.0',
            table='urn:oasis:names:tc:opendocument:xmlns:table:1.0',
            )
        try:
            with zipfile.ZipFile(filePath, 'r') as odfFile:
                content = odfFile.read('content.xml')
        except:
            raise Error(f'{_("Cannot read file")}: "{norm_path(filePath)}".')

        root = ET.fromstring(content)

        #--- Parse 'content.xml'.
        body = root.find('office:body', ns)
        spreadsheet = body.find('office:spreadsheet', ns)
        table = spreadsheet.find('table:table', ns)
        rows = []
        for row in table.findall('table:table-row', ns):
            cells = []
            i = 0
            for cell in row.findall('table:table-cell', ns):
                content = ''
                if cell.find('text:p', ns) is not None:
                    paragraphs = []
                    for par in cell.findall('text:p', ns):
                        strippedText = ''.join(par.itertext())
                        paragraphs.append(strippedText)
                    content = '\n'.join(paragraphs)
                    cells.append(content)
                elif i > 0:
                    cells.append(content)
                else:
                    # The ID cell is empty.
                    break

                i += 1
                if i >= cellsPerRow:
                    # The cell is excess, created by Calc.
                    break

                # Add repeated cells.
                attribute = cell.get(f'{{{ns["table"]}}}number-columns-repeated')
                if attribute:
                    repeat = int(attribute) - 1
                    for j in range(repeat):
                        if i >= cellsPerRow:
                            # The cell is excess, created by Calc.
                            break

                        cells.append(content)
                        i += 1
            if cells:
                rows.append(cells)
                # print(cells)
        return rows

