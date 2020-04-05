"""HmtlBookDescReader - Class for book summary. file operations and parsing.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from html.parser import HTMLParser

from pywriter.model.hform import *
from pywriter.collection.series import Series
from pywriter.collection.collection import Collection


class HmtlBookDescReader(HTMLParser):
    """HTML file representation of a book series containing
    a series summary and the series' book summaries 
    """

    _FILE_EXTENSION = 'html'

    def __init__(self, filePath):
        HTMLParser.__init__(self)
        self._seriesSummary = ''
        self._bookSummary = {}
        self._lines = []
        self._bkId = None
        self._collectText = False
        self._filePath = None
        self.filePath = filePath

    @property
    def filePath(self):
        return self._filePath

    @filePath.setter
    def filePath(self, filePath):
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
        """Recognize the end ot the series or book section and save data.
        Overwrites HTMLparser.handle_endtag().
        """
        if tag == 'div' and self._collectText:

            if self._bkId is None:
                self._seriesSummary = ''.join(self._lines)

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

    def read(self, series: Series, collection):
        """Parse the html file located at filePath, 
        fetching the Series and book descriptions.
        Return a message beginning with SUCCESS or ERROR.
        """
        result = read_html_file(self._filePath)

        if result[0].startswith('ERROR'):
            return (result[0])

        text = strip_markup(to_yw7(result[1]))

        # Invoke HTML parser.

        self.feed(text)

        series.summary = self._seriesSummary

        for bkId in self._bookSummary:
            collection.books[bkId].summary = self._bookSummary[bkId]

        return 'SUCCESS'
