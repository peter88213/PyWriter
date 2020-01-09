"""SceneDesc - Class for html scenes file operations and parsing.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from pywriter.edit.manuscript import Manuscript
from pywriter.convert.hform import *


HTML_HEADING_MARKERS = ("h3", "h2")
# Index is yWriter's chapter type:
# 0 is for an ordinary chapter
# 1 is for a chapter beginning a section


class SceneDesc(Manuscript):
    """HTML file representation of an yWriter project's scene descriptions part.

    Represents a html file with linkable chapter and scene sections 
    to be read and written by Open/LibreOffice Writer.

    # Attributes

    # Methods

    """

    def handle_endtag(self, tag):
        """HTML parser: Save scene content in dictionary at scene end. """

        if tag == 'div':
            if self.collectText:
                self.scenes[self.scID].desc = self.text
                self.text = ''
                self.collectText = False

    def write(self, novel) -> str:
        """Write attributes to html project file. """

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

        if novel.title is not None:
            if novel.title != '':
                self.title = novel.title

        if novel.scenes is not None:
            self.scenes = novel.scenes

        if novel.chapters is not None:
            self.chapters = novel.chapters

        text = HTML_HEADER.replace('$bookTitle$', self.title)
        text = text + '<h1>' + self.title + '</h1>'
        for chID in self.chapters:
            text = text + '<div id="ChID:' + chID + '">\n'
            headingMarker = HTML_HEADING_MARKERS[self.chapters[chID].type]
            text = text + '<' + headingMarker + '>' + \
                format_chapter_title(
                    self.chapters[chID].title) + '</' + headingMarker + '>\n'
            for scID in self.chapters[chID].scenes:
                text = text + '<div id="ScID:' + scID + '">\n'
                text = text + '<p class="firstlineindent">'
                text = text + '<a name="ScID:' + scID + '" />'
                # Insert scene ID as anchor.
                text = text + '<!-- ' + self.scenes[scID].title + ' -->\n'
                # Insert scene title as comment.
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
                # get_text() is to be overwritten
                # by file format specific subclasses.
        except(PermissionError):
            return('ERROR: ' + self._filePath + '" is write protected.')

        return('SUCCESS: "' + self._filePath + '" saved.')
