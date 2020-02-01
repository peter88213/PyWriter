"""Manuscript - Class for html manuscript file operations and parsing.

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


class Manuscript(PywFile, HTMLParser):
    """HTML file representation of an yWriter project's manuscript part.

    Represents a html file with chapter and scene sections 
    containing scene contents to be read and written by 
    OpenOffice/LibreOffice Writer.
    """

    _FILE_EXTENSION = 'html'
    # overwrites PywFile._FILE_EXTENSION

    def __init__(self, filePath: str) -> None:
        PywFile.__init__(self, filePath)
        HTMLParser.__init__(self)
        self._lines = []
        self._scId = None
        self._chId = None

    def handle_starttag(self, tag, attrs):
        """Recognize the beginning ot the body section.
        Overwrites HTMLparser.handle_starttag()
        """
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

    def handle_endtag(self, tag):
        """Recognize the end of the scene section and save data.
        Overwrites HTMLparser.handle_endtag().
        """
        if self._scId is not None:

            if tag == 'div':
                self.scenes[self._scId].sceneContent = ''.join(self._lines)
                self._lines = []
                self._scId = None

            elif tag == 'p':
                self._lines.append('\n')

        elif self._chId is not None:

            if tag == 'div':
                self._chId = None

    def handle_data(self, data):
        """Collect data within scene sections.
        Overwrites HTMLparser.handle_data().
        """
        if self._scId is not None:
            self._lines.append(data.rstrip().lstrip())

    def read(self) -> str:
        """Read scene content from a html file 
        with chapter and scene sections.
        Return a message beginning with SUCCESS or ERROR. 
        """

        result = read_html_file(self._filePath)

        if result[0].startswith('ERROR'):
            return (result[0])

        text = to_yw7(result[1])

        # Invoke HTML parser.

        self.feed(text)
        return 'SUCCESS: ' + str(len(self.scenes)) + ' Scenes read from "' + self._filePath + '".'

    def write(self, novel: Novel) -> str:
        """Generate a html file containing:
        - chapter sections containing:
            - chapter headings,
            - scene sections containing:
                - scene ID as anchor, 
                - scene title as comment,
                - scene content.
        Return a message beginning with SUCCESS or ERROR.
        """

        def format_chapter_title(text: str) -> str:
            """Fix auto-chapter titles for non-English """

            text = text.replace('Chapter ', '')
            return text

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

        lines = [HTML_HEADER.replace('$bookTitle$', self.title)]

        for chId in self.srtChapters:

            if (not self.chapters[chId].isUnused) and self.chapters[chId].chType == 0:
                lines.append('<div id="ChID:' + chId + '">')
                headingMarker = HTML_HEADING_MARKERS[self.chapters[chId].chLevel]
                lines.append('<' + headingMarker + '>' + format_chapter_title(
                    self.chapters[chId].title) + '</' + headingMarker + '>')

                for scId in self.chapters[chId].srtScenes:

                    if not self.scenes[scId].isUnused:
                        lines.append('<h4>' + HTML_SCENE_DIVIDER + '</h4>')
                        lines.append('<div id="ScID:' + scId + '">')
                        lines.append('<p class="textbody">')

                        # Insert scene ID as anchor.

                        lines.append('<a name="ScID:' + scId + '" />')

                        # Insert scene title as comment.

                        lines.append(
                            '<!-- ' + self.scenes[scId].title + ' -->')

                        if self.scenes[scId].sceneContent is not None:
                            lines.append(
                                to_html(self.scenes[scId].sceneContent))

                        lines.append('</p>')
                        lines.append('</div>')

                lines.append('</div>')

        lines.append(HTML_FOOTER)
        text = '\n'.join(lines)

        # Remove scene dividers from chapter's beginning

        text = text.replace('</h1>\n<h4>' + HTML_SCENE_DIVIDER + '</h4>',
                            '</h1>')
        text = text.replace('</h2>\n<h4>' + HTML_SCENE_DIVIDER + '</h4>',
                            '</h2>')

        try:
            with open(self._filePath, 'w', encoding='utf-8') as f:
                f.write(text)

        except(PermissionError):
            return 'ERROR: ' + self._filePath + '" is write protected.'

        return 'SUCCESS: "' + self._filePath + '" saved.'

    def get_structure(self) -> None:
        """This file format has no comparable structure."""
        return None
