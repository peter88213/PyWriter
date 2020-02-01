"""Collection - represents the basic structure of a collection of yWriter projects.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import re
import xml.etree.ElementTree as ET

from pywriter.collection.series import Series
from pywriter.collection.book import Book
from pywriter.model.xform import *


class Collection():
    """Represents collection of yWriter projects. 
    """

    _FILE_EXTENSION = 'pwc'

    def __init__(self, filePath: str) -> None:
        self.books = {}
        self.srtSeries = []
        self._filePath = None
        self.filePath = filePath
        self._cdataTags = ['Title', 'Desc', 'Path']

    @property
    def filePath(self) -> str:
        return self._filePath

    @filePath.setter
    def filePath(self, filePath: str) -> None:
        """Accept only filenames with the right extension. """
        if filePath.lower().endswith(self._FILE_EXTENSION):
            self._filePath = filePath

    def read(self) -> str:
        """Parse the pwc xml file located at filePath, 
        fetching the Collection attributes.
        Return a message beginning with SUCCESS or ERROR.
        """

        # Open the file and let ElementTree parse its xml structure.

        try:
            tree = ET.parse(self._filePath)
            root = tree.getroot()

        except:
            return 'ERROR: Can not process "' + self._filePath + '".'

        for srs in root.iter('SERIES'):
            newSeries = Series(srs.find('Title').text)

            if srs.find('Desc') is not None:
                newSeries.summary = srs.find('Desc').text

            newSeries.srtBooks = []

            if srs.find('Books') is not None:

                for boo in srs.find('Books').findall('BkID'):
                    bkId = boo.text
                    newSeries.srtBooks.append(bkId)

            self.srtSeries.append(newSeries)

        for boo in root.iter('BOOK'):
            bkId = boo.find('ID').text

            bookPath = boo.find('Path').text

            if os.path.isfile(bookPath):
                self.books[bkId] = Book(os.path.realpath(bookPath))

            else:
                return 'ERROR: Book "' + bookPath + '" not found.'

            '''
            self.books[bkId].title = boo.find('Title').text

            if boo.find('Desc') is not None:
                self.books[bkId].summary = boo.find('Desc').text
    
            self.books[bkId].wordCount = str(boo.find('WordCount').text)
            self.books[bkId].letterCount = str(boo.find('LetterCount').text)
            '''

        return 'SUCCESS: ' + str(len(self.books)) + ' Books found in "' + self._filePath + '".'

    def write(self) -> str:
        """Write the collection's attributes to a pwc xml file 
        located at filePath. Overwrite existing file without
        confirmation.
        Return a message beginning with SUCCESS or ERROR.
        """
        root = ET.Element('COLLECTION')
        bkSection = ET.SubElement(root, 'BOOKS')

        for bookId in self.books:
            self.books[bookId].put_book_data()
            newBook = ET.SubElement(bkSection, 'BOOK')
            bkId = ET.SubElement(newBook, 'ID')
            bkId.text = bookId
            '''
            bkTitle = ET.SubElement(newBook, 'Title')
            bkTitle.text = self.books[bookId].title
            bkDesc = ET.SubElement(newBook, 'Desc')
            bkDesc.text = self.books[bookId].summary
            bkWc = ET.SubElement(newBook, 'WordCount')
            bkWc.text = str(self.books[bookId].wordCount)
            bkLc = ET.SubElement(newBook, 'LetterCount')
            bkLc.text = str(self.books[bookId].letterCount)
            '''
            bkPath = ET.SubElement(newBook, 'Path')
            bkPath.text = self.books[bookId].filePath

        srSection = ET.SubElement(root, 'SRT_SERIES')

        for ser in self.srtSeries:
            newSeries = ET.SubElement(srSection, 'SERIES')
            serTitle = ET.SubElement(newSeries, 'Title')
            serTitle.text = ser.title
            serDesc = ET.SubElement(newSeries, 'Desc')
            serDesc.text = ser.summary
            serBooks = ET.SubElement(newSeries, 'Books')

            for bookId in ser.srtBooks:
                bkId = ET.SubElement(serBooks, 'BkID')
                bkId.text = bookId

        indent(root)
        tree = ET.ElementTree(root)

        try:
            tree.write(self._filePath, encoding='utf-8')

        except(PermissionError):
            return 'ERROR: "' + self._filePath + '" is write protected.'

        # Postprocess the xml file created by ElementTree
        message = cdata(self._filePath, self._cdataTags)

        if message.startswith('ERROR'):
            return message

        return 'SUCCESS: Collection written to "' + self._filePath + '".'

    def file_exists(self) -> bool:
        """Check whether the file specified by _filePath exists."""
        if os.path.isfile(self._filePath):
            return True
        else:
            return False

    def add_book(self, filePath: str) -> str:
        """Add an existing yWriter 7 project file as book to the 
        collection. Determine a book ID, read the novel's title and 
        description, and compute word count and letter count.
        Return a message beginning with SUCCESS or ERROR.
        """
        if os.path.isfile(filePath):
            filePath = os.path.realpath(filePath)
            i = 1
            while str(i) in self.books:
                i = i + 1

            bkId = str(i)
            self.books[bkId] = Book(filePath)
            return 'SUCCESS: "' + self.books[bkId].title + '" added to the collection.'

        else:
            return'ERROR: "' + os.path.realpath(filePath) + '" not found.'

    def remove_book(self, bkId: str) -> str:
        """Remove a book from the collection and from the series.
        Return a message beginning with SUCCESS or ERROR.
        """
        try:
            del self.books[bkId]

            for series in self.srtSeries:

                if series.remove_book(bkId).startswith('SUCCESS'):
                    return 'SUCCESS'

        except:
            return 'ERROR'

    def add_series(self, serTitle: str) -> None:
        """Instantiate a Series object and append it to the srtSeries list.
        """
        for series in self.srtSeries:
            if series.title == serTitle:
                return

        newSeries = Series(serTitle)
        self.srtSeries.append(newSeries)

    def remove_series(self, serTitle: str) -> str:
        """Delete a Series object and remove it from the srtSeries list.
        Return a message beginning with SUCCESS or ERROR.
        """
        for series in self.srtSeries:
            if series.title == serTitle:
                self.srtSeries.remove(series)
                return 'SUCCESS'

        return 'ERROR'
