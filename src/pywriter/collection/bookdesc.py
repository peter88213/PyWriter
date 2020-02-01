"""SceneDesc - Class for scene summary. file operations and parsing.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from html.parser import HTMLParser

from pywriter.model.hform import *
from pywriter.collection.book import Book
from pywriter.collection.series import Series
from pywriter.collection.collection import Collection


class BookDesc(HTMLParser):
    """HTML file representation of a series containing
    a series description and the series' book descriptions 
    """

    _FILE_EXTENSION = 'html'

    def __init__(self, filePath: str) -> None:
        HTMLParser.__init__(self)
        self._lines = []
        self._bkId = None
        self._desc = ''
        self._bookSummary = {}
        self._collectText = False
        self._filePath = None
        self.filePath = filePath

    @property
    def filePath(self) -> str:
        return self._filePath

    @filePath.setter
    def filePath(self, filePath: str) -> None:
        """Accept only filenames with the right extension. """
        if filePath.lower().endswith(self._FILE_EXTENSION):
            self._filePath = filePath

    def handle_starttag(self, tag, attrs):
        """Recognize the beginning of the book section.
        Overwrites HTMLparser.handle_starttag()
        """
        if tag == 'div':

            if attrs[0][0] == 'id':

                if attrs[0][1].startswith('SERIES'):
                    self._collectText = True

                if attrs[0][1].startswith('BkID'):
                    self._bkId = re.search('[0-9]+', attrs[0][1]).group()
                    self._collectText = True

    def handle_endtag(self, tag):
        """Recognize the end ot the book section and save data.
        Overwrites HTMLparser.handle_endtag().
        """
        if tag == 'div' and self._collectText:

            if self._bkId is None:
                self._desc = ''.join(self._lines)

            else:
                self._bookSummary[self._bkId] = ''.join(self._lines)

            self._lines = []
            self._collectText = False

        elif tag == 'p':
            self._lines.append('\n')

    def handle_data(self, data):
        """Cllect data within series and book sections.
        Overwrites HTMLparser.handle_data(). 
        """
        if self._collectText:
            self._lines.append(data.rstrip().lstrip())

    def read(self, series: Series, collection: Collection) -> str:
        """Parse the html file located at filePath, 
        fetching the Series and book descriptions.
        Return a message beginning with SUCCESS or ERROR.
        """

        try:
            with open(self._filePath, 'r', encoding='utf-8') as f:
                text = (f.read())
        except:
            # HTML files exported by a word processor may be ANSI encoded.
            try:
                with open(self._filePath, 'r') as f:
                    text = (f.read())

            except(FileNotFoundError):
                return '\nERROR: "' + self._filePath + '" not found.'

        text = to_yw7(text)

        # Invoke HTML parser.

        self.feed(text)

        series.summary = self._desc

        for bkId in self._bookSummary:
            collection.books[bkId].summary = self._bookSummary[bkId]

        return 'SUCCESS'

    def write(self, series: Series, collection: Collection) -> str:
        """Generate a html file containing:
        - A series sections containing:
            - series title heading,
            - series summary,
            - book sections containing:
                - book title heading,
                - book summary.
        Return a message beginning with SUCCESS or ERROR.
        """

        def to_html(text: str) -> str:
            """Convert yw7 raw markup """
            try:
                text = text.replace('\n\n', '\n')
                text = text.replace('\n', '</p>\n<p class="firstlineindent">')
            except:
                pass
            return text

        lines = [HTML_HEADER.replace('$bookTitle$', series.title)]
        lines.append('<h1>' + series.title + '</h1>\n')
        lines.append('<div id="SERIES">\n')
        lines.append('<p class="textbody">' + series.summary + '</p>\n')
        lines.append('</div>\n')

        for bkId in series.srtBooks:
            lines.append('<h2>' + collection.books[bkId].title + '</h2>\n')
            lines.append('<div id="BkID:' + bkId + '">\n')
            lines.append('<p class="textbody">')
            lines.append(to_html(collection.books[bkId].summary))
            lines.append('</p>\n')
            lines.append('</div>\n')

        lines.append(HTML_FOOTER)

        try:
            with open(self._filePath, 'w', encoding='utf-8') as f:
                f.writelines(lines)

        except(PermissionError):
            return 'ERROR: ' + self._filePath + '" is write protected.'

        return 'SUCCESS: "' + self._filePath + '" saved.'
