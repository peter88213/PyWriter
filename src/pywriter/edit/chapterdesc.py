"""SceneDesc - Class for html scenes file operations and parsing.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import re
from pywriter.core.chapter import Chapter
from pywriter.edit.manuscript import Manuscript


HTML_HEADING_MARKERS = ("h2", "h1")
# Index is yWriter's chapter type:
# 0 is for an ordinary chapter
# 1 is for a chapter beginning a section


STYLESHEET = '<style type="text/css">\n' + \
    'h1, h2, h3, h4, p {font: 1em monospace; margin: 3em; line-height: 1.5em}\n' + \
    'h1, h2, h3, h4 {text-align: center}\n' +\
    'h1 {letter-spacing: 0.5em; font-style: italic}' + \
    'h1, h2 {font-weight: bold}\n' + \
    'h3 {font-style: italic}\n' + \
    'p.textbody {margin-top:0; margin-bottom:0}\n' + \
    'p.firstlineindent {margin-top:0; margin-bottom:0; text-indent: 1em}\n' + \
    'strong {font-weight:normal; text-transform: uppercase}\n' + \
    '</style>\n'
# Make the generated html file look good in a web browser.

HTML_HEADER = '<html>\n' + '<head>\n' + \
    '<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>\n' + \
    STYLESHEET + \
    '<title>$bookTitle$</title>\n' + \
    '</head>\n' + '<body>\n'

HTML_FOOTER = '\n</body>\n</html>\n'


class ChapterDesc(Manuscript):
    """HTML file representation of an yWriter project's scene descriptions part.

    Represents a html file with linkable chapter and scene sections 
    to be read and written by Open/LibreOffice Writer.

    # Attributes

    # Methods

    """

    def handle_starttag(self, tag, attrs):
        """HTML parser: Get chapter ID at chapter start. """

        if tag == 'div':
            if attrs[0][0] == 'id':
                if attrs[0][1].startswith('ChID'):
                    self.chID = re.search('[0-9]+', attrs[0][1]).group()
                    self.chapters[self.chID] = Chapter()
                    self.collectText = True

    def handle_endtag(self, tag):
        """HTML parser: Save chapter description in dictionary at chapter end. """

        if tag == 'div':
            if self.collectText:
                self.chapters[self.chID].desc = self.text
                self.text = ''
                self.collectText = False

    def handle_data(self, data):
        """HTML parser: Collect paragraphs within scene. """

        if self.collectText:
            if data != ' ':
                self.text = self.text + data + '\n'

    def get_text(self):
        """Write attributes to html project file. """

        def format_chapter_title(text):
            """Fix auto-chapter titles for non-English """

            text = text.replace('Chapter ', '')
            return(text)

        text = HTML_HEADER.replace('$bookTitle$', self.title)
        for chID in self.chapters:
            headingMarker = HTML_HEADING_MARKERS[self.chapters[chID].type]
            text = text + '<' + headingMarker + '>' + \
                format_chapter_title(
                    self.chapters[chID].title) + '</' + headingMarker + '>\n'
            text = text + '<div id="ChID:' + chID + '">\n'
            text = text + '<p class="textbody">'
            text = text + '<a name="ChID:' + chID + '" />'
            # Insert chapter ID as anchor.
            try:
                text = text + (self.chapters[chID].desc)
            except(TypeError):
                text = text + ' '
            text = text + '</p>\n'
            text = text + '</div>\n'

        text = text + HTML_FOOTER
        return(text)
