"""Provide a class for html item invisibly tagged descriptions import.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import re

from pywriter.model.world_element import WorldElement
from pywriter.html.html_file import HtmlFile


class HtmlItems(HtmlFile):
    """HTML item descriptions file representation.

    Import a item sheet with invisibly tagged descriptions.
    """

    DESCRIPTION = 'Item descriptions'
    SUFFIX = '_items'

    def __init__(self, filePath, **kwargs):
        HtmlFile.__init__(self, filePath)
        self._itId = None

    def handle_starttag(self, tag, attrs):
        """Identify items.
        Overwrites HTMLparser.handle_starttag()
        """
        if tag == 'div':

            if attrs[0][0] == 'id':

                if attrs[0][1].startswith('ItID'):
                    self._itId = re.search('[0-9]+', attrs[0][1]).group()
                    self.srtItems.append(self._itId)
                    self.items[self._itId] = WorldElement()

    def handle_endtag(self, tag):
        """Recognize the end of the item section and save data.
        Overwrites HTMLparser.handle_endtag().
        """
        if self._itId is not None:

            if tag == 'div':
                self.items[self._itId].desc = ''.join(self._lines)
                self._lines = []
                self._itId = None

            elif tag == 'p':
                self._lines.append('\n')

    def handle_data(self, data):
        """collect data within item sections.
        Overwrites HTMLparser.handle_data().
        """
        if self._itId is not None:
            self._lines.append(data.rstrip().lstrip())
