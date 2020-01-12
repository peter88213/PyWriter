"""Manuscript - Class for html manuscript file operations and parsing.

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


class Manuscript(PywFile, HTMLParser):
    """HTML file representation of an yWriter project's manuscript part.

    Represents a html file with chapter and scene sections containing
    scene contents to be read and written by OpenOffice/LibreOffice 
    Writer.

    # Attributes

    _text : str
        contains the parsed data.

    _scId : str
        hands the Novel.scenes key over to the html parser

    _chId : str
        hands the Novel.chapters key over to the html parser

    _collectText : bool
        simple parsing state indicator. 
        True means: the data returned by the html parser 
        belongs to a scene section. 

    # Methods

    handle_starttag
        recognize the beginning ot the body section.
        Overwrites HTMLparser.handle_starttag()

    handle_endtag
        recognize the end ot the scene section and save data.
        Overwrites HTMLparser.handle_endtag()

    handle_data
        copy the body section.
        Overwrites HTMLparser.handle_data()

    read : str
        parse the html file located at filePath, fetching the Novel 
        attributes.
        Return a message beginning with SUCCESS or ERROR. 

    write : str
        Arguments 
            novel : Novel
                the data to be written. 
        Generate a html file containing:
        - chapter sections containing:
            - chapter heading,
            - scene sections containing:
                - scene ID as anchor 
                - scene title as comment
                - scene content
        Return a message beginning with SUCCESS or ERROR.
    """

    _fileExtension = 'html'
    # overwrites PywFile._fileExtension

    def __init__(self, filePath):
        PywFile.__init__(self, filePath)
        HTMLParser.__init__(self)
        self._text = ''
        self._scId = 0
        self._chId = 0
        self._collectText = False

    def handle_starttag(self, tag, attrs):
        """HTML parser: Get scene ID at scene start. """

        if tag == 'div':
            if attrs[0][0] == 'id':
                if attrs[0][1].startswith('ChID'):
                    self._chId = re.search('[0-9]+', attrs[0][1]).group()
                    self.chapters[self._chId] = Chapter()
                    self.chapters[self._chId].srtScenes = []
                    self.srtChapters.append(self._chId)

                elif attrs[0][1].startswith('ScID'):
                    self._scId = re.search('[0-9]+', attrs[0][1]).group()
                    self.scenes[self._scId] = Scene()
                    self.chapters[self._chId].srtScenes.append(self._scId)
                    self._collectText = True

    def handle_endtag(self, tag):
        """HTML parser: Save scene content in dictionary at scene end. """

        if tag == 'div':

            if self._collectText:
                self.scenes[self._scId].sceneContent = self._text
                self._text = ''
                self._collectText = False

    def handle_data(self, data):
        """HTML parser: Collect paragraphs within scene. """

        if self._collectText:

            if data != ' ':
                self._text = self._text + data + '\n'

    def read(self):
        """Read data from html file with chapter and scene sections. """

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
        return('SUCCESS: ' + str(len(self.scenes)) + ' Scenes read from "' + self._filePath + '".')

    def write(self, novel) -> str:
        """Write novel attributes to html file. """

        def format_chapter_title(text):
            """Fix auto-chapter titles for non-English """

            text = text.replace('Chapter ', '')
            return(text)

        # Copy the novel's attributes to write

        if novel.title is not None:
            if novel.title != '':
                self.title = novel.title

        if novel.srtChapters != []:
            self.srtChapters = novel.srtChapters

        if novel.scenes is not None:
            self.scenes = novel.scenes

        if novel.chapters is not None:
            self.chapters = novel.chapters

        text = HTML_HEADER.replace('$bookTitle$', self.title)

        for chId in self.srtChapters:
            text = text + '<div id="ChID:' + chId + '">\n'
            headingMarker = HTML_HEADING_MARKERS[self.chapters[chId].type]
            text = text + '<' + headingMarker + '>' + \
                format_chapter_title(
                    self.chapters[chId].title) + '</' + headingMarker + '>\n'

            for scId in self.chapters[chId].srtScenes:
                text = text + '<h4>' + HTML_SCENE_DIVIDER + '</h4>\n'
                text = text + '<div id="ScID:' + scId + '">\n'
                text = text + '<p class="textbody">'

                # Insert scene ID as anchor.

                text = text + '<a name="ScID:' + scId + '" />'

                # Insert scene title as comment.

                text = text + '<!-- ' + self.scenes[scId].title + ' -->\n'

                try:
                    text = text + \
                        to_html(self.scenes[scId].sceneContent)

                except(TypeError):
                    text = text + ' '

                text = text + '</p>\n'
                text = text + '</div>\n'

            text = text + '</div>\n'

        # Remove scene dividers from chapter's beginning

        text = text.replace('</h1>\n<h4>' + HTML_SCENE_DIVIDER + '</h4>',
                            '</h1>')
        text = text.replace('</h2>\n<h4>' + HTML_SCENE_DIVIDER + '</h4>',
                            '</h2>')
        text = text + HTML_FOOTER

        try:
            with open(self._filePath, 'w', encoding='utf-8') as f:
                f.write(text)

        except(PermissionError):
            return('ERROR: ' + self._filePath + '" is write protected.')

        return('SUCCESS: "' + self._filePath + '" saved.')
