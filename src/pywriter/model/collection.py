"""Collection - represents the basic structure of a collection of yWriter projects.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import re
import xml.etree.ElementTree as ET

from pywriter.model.series import Series
from pywriter.model.book import Book


class Collection():
    """yWriter project representation. 

    # Attributes

    desc : str
        the novel summary.

    books : dict
        key = scene ID, value = Book object.
        The order of the elements does not matter.

    srtSeries : list 
        the collection's series IDs.

    # Properties

    filePath : str (property with setter)
        Path to the file.
        The setter only accepts files of a supported type as specified 
        by _fileExtension. 

    # Methods 

    read : str
        parse the pwc xml file located at filePath, fetching the 
        Collection attributes.
        Return a message beginning with SUCCESS or ERROR. 

    write : str
        Open the pwc xml file located at filePath and replace a set 
        of items by the novel attributes not being None.
        Return a message beginning with SUCCESS or ERROR.

    file_exists() : bool
        True means: the file specified by filePath exists. 
    """

    _fileExtension = 'pwc'

    def __init__(self, filePath):
        self.books = {}
        self.srtSeries = []
        self._filePath = None
        self.filePath = filePath
        self._cdataTags = ['Title', 'Desc', 'Path']

    @property
    def filePath(self):
        return(self._filePath)

    @filePath.setter
    def filePath(self, filePath):
        """Accept only filenames with the right extension. """
        if filePath.lower().endswith(self._fileExtension):
            self._filePath = filePath

    def read(self) -> str:
        """Parse yw7 xml project file and store selected attributes. """

        # Open the file and let ElementTree parse its xml structure.

        try:
            tree = ET.parse(self._filePath)
            root = tree.getroot()

        except:
            return('ERROR: Can not process "' + self._filePath + '".')

        for srs in root.iter('SERIES'):
            newSeries = Series()
            newSeries.title = srs.find('Title').text

            if srs.find('Desc') is not None:
                newSeries.desc = srs.find('Desc').text

            newSeries.srtBooks = []

            if srs.find('Books') is not None:

                for boo in srs.find('Books').findall('BkID'):
                    bkId = boo.text
                    newSeries.srtBooks.append(bkId)

            self.srtSeries.append(newSeries)

        for boo in root.iter('BOOK'):
            bkId = boo.find('ID').text
            self.books[bkId] = Book()
            self.books[bkId].title = boo.find('Title').text

            if boo.find('Desc') is not None:
                self.books[bkId].desc = boo.find('Desc').text

            self.books[bkId].wordCount = str(boo.find('WordCount').text)
            self.books[bkId].letterCount = str(boo.find('LetterCount').text)
            self.books[bkId].filePath = boo.find('Path').text

        return('SUCCESS: ' + str(len(self.books)) + ' Books found in"' + self._filePath + '".')

    def write(self):
        """Write the collection's structure to the configuration file. """

        root = ET.Element('COLLECTION')
        bkSection = ET.SubElement(root, 'BOOKS')

        for bookId in self.books:
            newBook = ET.SubElement(bkSection, 'BOOK')
            bkId = ET.SubElement(newBook, 'ID')
            bkId.text = bookId
            bkTitle = ET.SubElement(newBook, 'Title')
            bkTitle.text = self.books[bookId].title
            bkDesc = ET.SubElement(newBook, 'Desc')
            bkDesc.text = self.books[bookId].desc
            bkWc = ET.SubElement(newBook, 'WordCount')
            bkWc.text = str(self.books[bookId].wordCount)
            bkLc = ET.SubElement(newBook, 'LetterCount')
            bkLc.text = str(self.books[bookId].letterCount)
            bkPath = ET.SubElement(newBook, 'Path')
            bkPath.text = self.books[bookId].filePath

        srSection = ET.SubElement(root, 'SRT_SERIES')

        for ser in self.srtSeries:
            newSeries = ET.SubElement(srSection, 'SERIES')
            serTitle = ET.SubElement(newSeries, 'Title')
            serTitle.text = ser.title
            serDesc = ET.SubElement(newSeries, 'Desc')
            serDesc.text = ser.desc
            serBooks = ET.SubElement(newSeries, 'Books')

            for bookId in ser.srtBooks:
                bkId = ET.SubElement(serBooks, 'BkID')
                bkId.text = bookId

        tree = ET.ElementTree(root)

        try:
            tree.write(self._filePath, encoding='utf-8')

        except(PermissionError):
            return('ERROR: "' + self._filePath + '" is write protected.')

        # Postprocess the xml file created by ElementTree:
        # Put a header on top and insert the missing CDATA tags.

        newXml = '<?xml version="1.0" encoding="utf-8"?>\n'
        with open(self._filePath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

            for line in lines:

                for tag in self._cdataTags:
                    line = re.sub('\<' + tag + '\>', '<' +
                                  tag + '><![CDATA[', line)
                    line = re.sub('\<\/' + tag + '\>',
                                  ']]></' + tag + '>', line)

                newXml = newXml + line

        newXml = newXml.replace('\n \n', '\n')
        newXml = newXml.replace('[CDATA[ \n', '[CDATA[')
        newXml = newXml.replace('\n]]', ']]')

        newXml = newXml.replace('><', '>\n<')

        try:
            with open(self._filePath, 'w', encoding='utf-8') as f:
                f.write(newXml)

        except:
            return('ERROR: Can not write"' + self._filePath + '".')

        return('SUCCESS: Collection written to "' + self._filePath + '".')

    def file_exists(self) -> bool:
        """Check whether the file specified by _filePath exists. """

        if os.path.isfile(self._filePath):
            return(True)

        else:
            return(False)
