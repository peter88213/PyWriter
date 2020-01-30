"""HtmlFile - Class for html file operations and parsing.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from html.parser import HTMLParser

from pywriter.model.novel import Novel
from pywriter.model.pywfile import PywFile
from pywriter.model.chapter import Chapter
from pywriter.model.scene import Scene
from pywriter.model.hform import *

HTML_HEADING_MARKERS = ("h2", "h1")
# Index is yWriter's chapter chLevel:
# 0 is for an ordinary chapter
# 1 is for a chapter beginning a section


class HtmlFile(PywFile, HTMLParser):
    """HTML file representation of an yWriter project's OfficeFile part.

    Represents a html file with visible chapter and scene tags 
    to be read and written by Open/LibreOffice Writer.

    # Attributes

    _lines : str
        contains the parsed data.

    _collectText : bool
        simple parsing state indicator. 
        True means: the data returned by the html parser 
        belongs to the body section. 

    # Methods

    handle_starttag
        recognize the beginning of the body section.
        Overwrites HTMLparser.handle_starttag()

    handle_endtag
        recognize the end of the body section.
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
        - chapter ID tags,
        - chapter headings,
        - scene ID tags, 
        - scene content.
        Return a message beginning with SUCCESS or ERROR.
    """

    _FILE_EXTENSION = 'html'
    # overwrites PywFile._FILE_EXTENSION

    def __init__(self, filePath: str) -> None:
        PywFile.__init__(self, filePath)
        HTMLParser.__init__(self)
        self._lines = []
        self._collectText = False

    def handle_starttag(self, tag, attrs):
        """Recognize the beginning ot the body section. """

        if tag == 'p':
            self._collectText = True

    def handle_endtag(self, tag):
        """Recognize the end ot the body section. """

        if tag == 'p':
            self._collectText = False

    def handle_data(self, data):
        """Copy paragraphs. """

        if self._collectText:
            self._lines.append(data)

    def read(self) -> str:
        """Read data from html file with chapter and scene tags. """

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

        # Invoke HTML parser to write the html body as raw text
        # to self._lines.

        self.feed(text)

        # Parse the HTML body to identify chapters and scenes.

        sceneText = []
        scId = ''
        chId = ''
        inScene = False

        for line in self._lines:

            if line.startswith('[ScID'):
                scId = re.search('[0-9]+', line).group()
                self.scenes[scId] = Scene()
                self.chapters[chId].srtScenes.append(scId)
                inScene = True

            elif line.startswith('[/ScID'):
                self.scenes[scId].sceneContent = '\n'.join(sceneText)
                sceneText = []
                inScene = False

            elif line.startswith('[ChID'):
                chId = re.search('[0-9]+', line).group()
                self.chapters[chId] = Chapter()
                self.srtChapters.append(chId)

            elif line.startswith('[/ChID'):
                pass

            elif inScene:
                sceneText.append(line)

        return 'SUCCESS: ' + str(len(self.scenes)) + ' Scenes read from "' + self._filePath + '".'

    def write(self, novel: Novel) -> str:
        """Write novel attributes to html file. """

        def format_chapter_title(text):
            """Fix auto-chapter titles for non-English """

            text = text.replace('Chapter ', '')
            return text

        # Copy the novel's attributes to write

        if novel.title is not None:

            if novel.title is not None:
                self.title = novel.title

        if novel.srtChapters != []:
            self.srtChapters = novel.srtChapters

        self.scenes = novel.scenes
        self.chapters = novel.chapters

        lines = [HTML_HEADER.replace('$bookTitle$', self.title)]

        for chId in self.srtChapters:

            if self.chapters[chId].isUnused:
                lines.append(
                    '<p style="font-size:x-small">[ChID:' + chId + ' (Unused)]</p>')

            else:
                lines.append(
                    '<p style="font-size:x-small">[ChID:' + chId + ']</p>')

            headingMarker = HTML_HEADING_MARKERS[self.chapters[chId].chLevel]
            lines.append('<' + headingMarker + '>' + format_chapter_title(
                self.chapters[chId].title) + '</' + headingMarker + '>')

            for scId in self.chapters[chId].srtScenes:
                lines.append('<h4>' + HTML_SCENE_DIVIDER + '</h4>')

                if self.scenes[scId].isUnused:
                    lines.append(
                        '<p style="font-size:x-small">[ScID:' + scId + ' (Unused)]</p>')

                else:
                    lines.append(
                        '<p style="font-size:x-small">[ScID:' + scId + ']</p>')

                if self.scenes[scId].sceneContent is not None:
                    lines.append('<p class="textbody">' +
                                 to_html(self.scenes[scId].sceneContent) + '</p>')

                if self.scenes[scId].isUnused:
                    lines.append(
                        '<p style="font-size:x-small">[/ScID (Unused)]</p>')

                else:
                    lines.append('<p style="font-size:x-small">[/ScID]</p>')

            if self.chapters[chId].isUnused:
                lines.append(
                    '<p style="font-size:x-small">[/ChID (Unused)]</p>')

            else:
                lines.append('<p style="font-size:x-small">[/ChID]</p>')

        lines.append(HTML_FOOTER)
        text = '\n'.join(lines)

        # Remove scene dividers from chapter's beginning

        text = text.replace(
            '</h1>\n<h4>' + HTML_SCENE_DIVIDER + '</h4>', '</h1>')
        text = text.replace(
            '</h2>\n<h4>' + HTML_SCENE_DIVIDER + '</h4>', '</h2>')

        try:
            with open(self._filePath, 'w', encoding='utf-8') as f:
                f.write(text)

        except(PermissionError):
            return 'ERROR: ' + self._filePath + '" is write protected.'

        return 'SUCCESS: "' + self._filePath + '" saved.'
