"""HtmlFile - Class for html file operations and parsing.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from html.parser import HTMLParser

from pywriter.model.pywfile import PywFile
from pywriter.model.chapter import Chapter
from pywriter.model.scene import Scene
from pywriter.model.hform import *

HTML_HEADING_MARKERS = ("h2", "h1")
# Index is yWriter's chapter type:
# 0 is for an ordinary chapter
# 1 is for a chapter beginning a section


class HtmlFile(PywFile, HTMLParser):
    """HTML file representation of an yWriter project's OfficeFile part.

    Represents a html file visible chapter and scene tags 
    to be read and written by Open/LibreOffice Writer.

    # Attributes

    _text : str
        contains the parsed data.
    _collectText : bool
        simple parsing state indicator. 
        True means: the data returned by the html parser 
        belongs to the body section. 

    # Methods

    read : str
        parse the htmml file located at filePath, fetching the Novel 
        attributes.
        Return a message beginning with SUCCESS or ERROR. 
    write : str
        open the html file located at filePath and replace a set of 
        items by the Novel attributes not being None.
        Return a message beginning with SUCCESS or ERROR.
    handle_starttag
        recognize the beginning ot the body section.
        Overwrites HTMLparser.handle_starttag()
    handle_endtag
        recognize the end ot the body section.
        Overwrites HTMLparser.handle_endtag()
    handle_data
        copy the body section.
        Overwrites HTMLparser.handle_data()
    """

    _fileExtension = 'html'

    def __init__(self, filePath):
        PywFile.__init__(self, filePath)
        HTMLParser.__init__(self)
        self._text = ''
        self._collectText = False

    def read(self):
        """Read data from html project file. """

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

        # Invoke HTML parser to write the html body as raw text
        # to self._text.

        self.feed(text)

        sceneText = ''
        scID = ''
        chID = ''
        inScene = False
        lines = self._text.split('\n')

        for line in lines:

            if line.startswith('[ScID'):
                scID = re.search('[0-9]+', line).group()
                self.scenes[scID] = Scene()
                self.chapters[chID].scenes.append(scID)
                inScene = True

            elif line.startswith('[/ScID]'):
                self.scenes[scID].sceneContent = sceneText
                sceneText = ''
                inScene = False

            elif line.startswith('[ChID'):
                chID = re.search('[0-9]+', line).group()
                self.chapters[chID] = Chapter()

            elif line.startswith('[/ChID]'):
                pass

            elif inScene:
                sceneText = sceneText + line + '\n'

        return('SUCCESS: ' + str(len(self.scenes)) + ' Scenes read from "' + self._filePath + '".')

    def write(self, novel) -> str:
        """Write attributes to html project file. """

        def format_chapter_title(text):
            """Fix auto-chapter titles for non-English """

            text = text.replace('Chapter ', '')
            return(text)

        if novel.title is not None:
            if novel.title != '':
                self.title = novel.title

        if novel.scenes is not None:
            self.scenes = novel.scenes

        if novel.chapters is not None:
            self.chapters = novel.chapters

        text = HTML_HEADER.replace('$bookTitle$', self.title)
        for chID in self.chapters:
            text = text + \
                '<p style="font-size:x-small">[ChID:' + chID + ']</p>\n'
            headingMarker = HTML_HEADING_MARKERS[self.chapters[chID].type]
            text = text + '<' + headingMarker + '>' + \
                format_chapter_title(
                    self.chapters[chID].title) + '</' + headingMarker + '>\n'
            for scID in self.chapters[chID].scenes:
                text = text + '<h4>' + HTML_SCENE_DIVIDER + '</h4>\n'
                text = text + \
                    '<p style="font-size:x-small">[ScID:' + scID + ']</p>\n'
                text = text + '<p class="textbody">'
                try:
                    text = text + \
                        to_html(self.scenes[scID].sceneContent)
                except(TypeError):
                    text = text + ' '
                text = text + '</p>\n'
                text = text + '<p style="font-size:x-small">[/ScID]</p>\n'

            text = text + '<p style="font-size:x-small">[/ChID]</p>\n'
        text = text.replace(
            '</h1>\n<h4>' + HTML_SCENE_DIVIDER + '</h4>', '</h1>')
        text = text.replace(
            '</h2>\n<h4>' + HTML_SCENE_DIVIDER + '</h4>', '</h2>')
        text = text + HTML_FOOTER

        try:
            with open(self._filePath, 'w', encoding='utf-8') as f:
                f.write(text)

        except(PermissionError):
            return('ERROR: ' + self._filePath + '" is write protected.')

        return('SUCCESS: "' + self._filePath + '" saved.')

    def handle_starttag(self, tag, attrs):
        """Recognize the beginning ot the body section. """

        if tag == 'body':
            self._collectText = True

    def handle_endtag(self, tag):
        """Recognize the end ot the body section. """

        if tag == 'body':
            self._collectText = False

    def handle_data(self, data):
        """Copy the body section. """

        if self._collectText:
            self._text = self._text + data + '\n'
            # Get the html body.
