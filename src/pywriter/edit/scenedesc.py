"""SceneDesc - Class for html scenes file operations and parsing.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from pywriter.edit.manuscript import Manuscript


HTML_HEADING_MARKERS = ("h3", "h2")
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

    def get_text(self):
        """Write attributes to html project file. """

        def format_chapter_title(text):
            """Fix auto-chapter titles for non-English """

            text = text.replace('Chapter ', '')
            return(text)

        def format_yw7(text):
            """Convert yw7 raw markup """
            try:
                text = text.replace('\n\n', '\n')
                text = text.replace('\n', '</p>\n<p class="firstlineindent">')
            except:
                pass
            return(text)

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
                    text = text + format_yw7(self.scenes[scID].desc)
                except(TypeError):
                    text = text + ' '
                text = text + '</p>\n'
                text = text + '</div>\n'

            text = text + '</div>\n'
        text = text + HTML_FOOTER
        return(text)
