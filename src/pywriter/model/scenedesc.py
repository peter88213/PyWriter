"""SceneDesc - Class for scene desc. file operations and parsing.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from pywriter.model.manuscript import Manuscript
from pywriter.model.hform import *


HTML_HEADING_MARKERS = ("h3", "h2")
# Index is yWriter's chapter type:
# 0 is for an ordinary chapter
# 1 is for a chapter beginning a section


class SceneDesc(Manuscript):
    """HTML file representation of an yWriter project's scene descriptions part.

    Represents a html file with chapter and scene sections containing 
    scene descriptions to be read and written by OpenOffice /LibreOffice 
    Writer.

    # Methods

    handle_endtag
        recognize the end ot the scene section and save data.
        Overwrites HTMLparser.handle_endtag()

    write : str
        Arguments 
            novel : Novel
                the data to be written. 
        Generate a html file containing:
        - chapter sections containing:
            - chapter headings,
            - scene sections containing:
                - scene ID as anchor 
                - scene title as comment
                - scene description
        Return a message beginning with SUCCESS or ERROR.
    """

    def handle_endtag(self, tag):
        """HTML parser: Save scene description in dictionary at scene end. """

        if tag == 'div':
            if self._collectText:
                self.scenes[self._scId].desc = self._text
                self._text = ''
                self._collectText = False

    def write(self, novel) -> str:
        """Write novel attributes to html file.  """

        def format_chapter_title(text):
            """Fix auto-chapter titles for non-English """
            text = text.replace('Chapter ', '')
            return(text)

        def to_html(text):
            """Convert yw7 raw markup """
            try:
                text = text.replace('\n\n', '\n')
                text = text.replace('\n', '</p>\n<p class="firstlineindent">')
            except:
                pass
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
        text = text + '<h1>' + self.title + '</h1>'

        for chID in self.srtChapters:
            text = text + '<div id="ChID:' + chID + '">\n'
            headingMarker = HTML_HEADING_MARKERS[self.chapters[chID].type]
            text = text + '<' + headingMarker + '>' + format_chapter_title(
                self.chapters[chID].title) + '</' + headingMarker + '>\n'

            for scID in self.chapters[chID].srtScenes:
                text = text + '<div id="ScID:' + scID + '">\n'
                text = text + '<p class="firstlineindent">'

                # Insert scene ID as anchor.

                text = text + '<a name="ScID:' + scID + '" />'

                # Insert scene title as comment.

                text = text + '<!-- ' + self.scenes[scID].title + ' -->\n'

                try:
                    text = text + to_html(self.scenes[scID].desc)

                except(TypeError):
                    text = text + ' '

                text = text + '</p>\n'
                text = text + '</div>\n'

            text = text + '</div>\n'

        text = text + HTML_FOOTER

        try:
            with open(self._filePath, 'w', encoding='utf-8') as f:
                f.write(text)

        except(PermissionError):
            return('ERROR: ' + self._filePath + '" is write protected.')

        return('SUCCESS: "' + self._filePath + '" saved.')
