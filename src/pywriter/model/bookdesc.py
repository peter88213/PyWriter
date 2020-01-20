"""SceneDesc - Class for scene desc. file operations and parsing.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from html.parser import HTMLParser
from pywriter.model.hform import *

from pywriter.model.book import Book
from cgitb import text


class BookDesc(HTMLParser):
    """HTML file representation of a series' book descriptions.

    Represents a html file with book sections containing 
    book descriptions to be read and written by OpenOffice /LibreOffice 
    Writer.

    # Properties

    filePath : str (property with setter)
        Path to the file.
        The setter only accepts files of a supported type as specified 
        by _fileExtension. 

    # Methods

    handle_starttag
        recognize the beginning ot the book section.
        Overwrites HTMLparser.handle_starttag()

    handle_endtag
        recognize the end ot the book section and save data.
        Overwrites HTMLparser.handle_endtag()

    handle_data
        copy the book description.
        Overwrites HTMLparser.handle_data()

    read : str
        parse the html file located at filePath, fetching the Series 
        attributes.
        Return a message beginning with SUCCESS or ERROR. 

    write : str
        Arguments 
            series : Series
            collection : Collection
        Generate a html file containing:
        - a series section containing:
            - series title
            - series description
        - book sections containing:
            - book title heading
            - book description
        Return a message beginning with SUCCESS or ERROR.
    """

    _fileExtension = 'html'
    # overwrites PywFile._fileExtension

    def __init__(self, filePath):
        HTMLParser.__init__(self)
        self._text = ''
        self._bkId = None
        self._desc = ''
        self._bookDesc = {}
        self._collectText = False
        self._filePath = None
        self.filePath = filePath

    @property
    def filePath(self):
        return(self._filePath)

    @filePath.setter
    def filePath(self, filePath):
        """Accept only filenames with the right extension. """
        if filePath.lower().endswith(self._fileExtension):
            self._filePath = filePath

    def handle_starttag(self, tag, attrs):
        """HTML parser: Get book ID at book start. """

        if tag == 'div':

            if attrs[0][0] == 'id':

                if attrs[0][1].startswith('SERIES'):
                    self._collectText = True

                if attrs[0][1].startswith('BkID'):
                    self._bkId = re.search('[0-9]+', attrs[0][1]).group()
                    self._collectText = True

    def handle_endtag(self, tag):
        """HTML parser: Save chapter description in dictionary at chapter end. """

        if tag == 'div' and self._collectText:

            if self._bkId is None:
                self._desc = self._text

            else:
                self._bookDesc[self._bkId] = self._text

            self._text = ''
            self._collectText = False

    def handle_data(self, data):
        """HTML parser: Collect paragraphs within chapter description. """

        if self._collectText:
            self._text = self._text + data + '\n'

    def read(self, series, collection) -> str:
        """Read series attributes from html file.  """

        try:
            with open(self._filePath, 'r', encoding='utf-8') as f:
                text = (f.read())
        except:
            # HTML files exported by a word processor may be ANSI encoded.
            try:
                with open(self._filePath, 'r') as f:
                    text = (f.read())

            except(FileNotFoundError):
                return('\nERROR: "' + self._filePath + '" not found.')

        text = to_yw7(text)

        # Invoke HTML parser.

        self.feed(text)

        series.desc = self._desc

        for bkId in self._bookDesc:
            collection.books[bkId].desc = self._bookDesc[bkId]

        return('SUCCESS')

    def write(self, series, collection) -> str:
        """Write series attributes to html file.  """

        def to_html(text):
            """Convert yw7 raw markup """
            try:
                text = text.replace('\n\n', '\n')
                text = text.replace('\n', '</p>\n<p class="firstlineindent">')
            except:
                pass
            return(text)

        text = HTML_HEADER.replace('$bookTitle$', series.title)
        text = text + '<h1>' + series.title + '</h1>\n'
        text = text + '<div id="SERIES">\n'
        text = text + '<p class="textbody">' + series.desc + '</p>\n'
        text = text + '</div>\n'

        for bkId in series.srtBooks:
            text = text + '<h2>' + collection.books[bkId].title + '</h2>\n'
            text = text + '<div id="BkID:' + bkId + '">\n'
            text = text + '<p class="textbody">'
            text = text + to_html(collection.books[bkId].desc)
            text = text + '</p>\n'
            text = text + '</div>\n'

        text = text + HTML_FOOTER

        try:
            with open(self._filePath, 'w', encoding='utf-8') as f:
                f.write(text)

        except(PermissionError):
            return('ERROR: ' + self._filePath + '" is write protected.')

        return('SUCCESS: "' + self._filePath + '" saved.')
