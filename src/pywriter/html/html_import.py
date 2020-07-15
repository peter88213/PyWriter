"""HtmlImport - Class for html import file parsing.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from pywriter.html.html_manuscript import HtmlManuscript
from pywriter.html.html_form import *
from pywriter.model.chapter import Chapter
from pywriter.model.scene import Scene


class HtmlImport(HtmlManuscript):
    """HTML file representation of an yWriter project's OfficeFile part.

    Represents a html file without chapter and scene tags 
    to be written by Open/LibreOffice Writer.
    """

    SUFFIX = ''

    _SCENE_DIVIDER = '* * *'
    _LOW_WORDCOUNT = 10

    def __init__(self, filePath):
        HtmlManuscript.__init__(self, filePath)
        self._chCount = 0
        self._scCount = 0

    def handle_starttag(self, tag, attrs):

        if tag in ('h1', 'h2'):
            self._scId = None
            self._lines = []
            self._chCount += 1
            self._chId = str(self._chCount)
            self.chapters[self._chId] = Chapter()
            self.chapters[self._chId].srtScenes = []
            self.srtChapters.append(self._chId)
            self.chapters[self._chId].chType = '0'

            if tag == 'h1':
                self.chapters[self._chId].chLevel = 1

            else:
                self.chapters[self._chId].chLevel = 0

        elif tag == 'p':

            if self._scId is None and self._chId is not None:
                self._lines = []
                self._scCount += 1
                self._scId = str(self._scCount)
                self.scenes[self._scId] = Scene()
                self.chapters[self._chId].srtScenes.append(self._scId)
                self.scenes[self._scId].status = '1'
                self.scenes[self._scId].title = 'Scene ' + str(self._scCount)

        elif tag == 'div':
            self._scId = None
            self._chId = None

        elif tag == 'meta':

            if attrs[0][1].lower() == 'author':
                self.author = attrs[1][1]

            if attrs[0][1].lower() == 'description':
                self.desc = attrs[1][1]

        elif tag == 'title':
            self._lines = []

    def handle_endtag(self, tag):

        if tag == 'p':
            self._lines.append('\n')

            if self._scId is not None:
                self.scenes[self._scId].sceneContent = ''.join(self._lines)

                if self.scenes[self._scId].wordCount < self._LOW_WORDCOUNT:
                    self.scenes[self._scId].status = 1

                else:
                    self.scenes[self._scId].status = 2

        elif tag in ('h1', 'h2'):
            self.chapters[self._chId].title = ''.join(self._lines)
            self._lines = []

        elif tag == 'title':
            self.title = ''.join(self._lines)

    def handle_data(self, data):
        """Collect data within scene sections.
        Overwrites HTMLparser.handle_data().
        """
        if self._scId is not None and self._SCENE_DIVIDER in data:
            self._scId = None

        else:
            self._lines.append(data.rstrip().lstrip())
