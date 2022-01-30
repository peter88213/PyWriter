"""Provide a generic class for html file import.

Other html file representations inherit from this class.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import re
from html.parser import HTMLParser

from pywriter.pywriter_globals import ERROR
from pywriter.model.novel import Novel
from pywriter.model.chapter import Chapter
from pywriter.model.scene import Scene
from pywriter.html.html_fop import read_html_file


class HtmlFile(Novel, HTMLParser):
    """Generic HTML file representation."""

    EXTENSION = '.html'
    COMMENT_START = '/*'
    COMMENT_END = '*/'
    SC_TITLE_BRACKET = '~'

    def __init__(self, filePath, **kwargs):
        super().__init__(filePath)
        HTMLParser.__init__(self)
        self._lines = []
        self._scId = None
        self._chId = None

    def convert_to_yw(self, text):
        """Convert html tags to yWriter 6/7 raw markup. 
        Return a yw6/7 markup string.
        """

        # Clean up polluted HTML code.

        text = re.sub('</*font.*?>', '', text)
        text = re.sub('</*span.*?>', '', text)
        text = re.sub('</*FONT.*?>', '', text)
        text = re.sub('</*SPAN.*?>', '', text)

        # Put everything in one line.

        text = text.replace('\n', ' ')
        text = text.replace('\r', ' ')
        text = text.replace('\t', ' ')

        while '  ' in text:
            text = text.replace('  ', ' ').strip()

        # Replace HTML tags by yWriter markup.

        text = text.replace('<i>', '[i]')
        text = text.replace('<I>', '[i]')
        text = text.replace('</i>', '[/i]')
        text = text.replace('</I>', '[/i]')
        text = text.replace('</em>', '[/i]')
        text = text.replace('</EM>', '[/i]')
        text = text.replace('<b>', '[b]')
        text = text.replace('<B>', '[b]')
        text = text.replace('</b>', '[/b]')
        text = text.replace('</B>', '[/b]')
        text = text.replace('</strong>', '[/b]')
        text = text.replace('</STRONG>', '[/b]')
        text = re.sub('<em.*?>', '[i]', text)
        text = re.sub('<EM.*?>', '[i]', text)
        text = re.sub('<strong.*?>', '[b]', text)
        text = re.sub('<STRONG.*?>', '[b]', text)

        # Remove orphaned tags.

        text = text.replace('[/b][b]', '')
        text = text.replace('[/i][i]', '')
        text = text.replace('[/b][b]', '')

        # Convert author's comments

        text = text.replace('<!--', '/*')
        text = text.replace('-->', '*/')

        return text

    def preprocess(self, text):
        """Clean up the HTML code and strip yWriter 6/7 raw markup. 
        This prevents accidentally applied formatting from being 
        transferred to the yWriter metadata. If rich text is 
        applicable, such as in scenes, overwrite this method 
        in a subclass) 
        """
        text = self.convert_to_yw(text)

        # Remove misplaced formatting tags.

        text = re.sub('\[\/*[b|i]\]', '', text)
        return text

    def postprocess(self):
        """Process the plain text after parsing.
        This is a hook for subclasses.
        """

    def handle_starttag(self, tag, attrs):
        """Identify scenes and chapters.
        Override HTMLparser.handle_starttag().
        This method is applicable to HTML files that are divided into 
        chapters and scenes. For differently structured HTML files 
        do override this method in a subclass.
        """
        if tag == 'div':

            if attrs[0][0] == 'id':

                if attrs[0][1].startswith('ScID'):
                    self._scId = re.search('[0-9]+', attrs[0][1]).group()
                    self.scenes[self._scId] = Scene()
                    self.chapters[self._chId].srtScenes.append(self._scId)

                elif attrs[0][1].startswith('ChID'):
                    self._chId = re.search('[0-9]+', attrs[0][1]).group()
                    self.chapters[self._chId] = Chapter()
                    self.chapters[self._chId].srtScenes = []
                    self.srtChapters.append(self._chId)

    def read(self):
        """Read and parse a html file, fetching the Novel attributes.
        Return a message beginning with the ERROR constant in case of error.
        This is a template method for subclasses tailored to the 
        content of the respective HTML file.
        """
        result = read_html_file(self.filePath)

        if result[0].startswith(ERROR):
            return (result[0])

        text = self.preprocess(result[1])
        self.feed(text)
        self.postprocess()

        return 'Created novel structure from HTML data.'
