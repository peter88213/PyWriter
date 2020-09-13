"""HtmlLocations - Class for html location description file parsing.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import re

from pywriter.model.object import Object
from pywriter.html.html_file import HtmlFile


class HtmlLocations(HtmlFile):
    """HTML file representation of an yWriter project's location descriptions."""

    DESCRIPTION = 'Location descriptions'
    SUFFIX = '_locations'

    def __init__(self, filePath):
        HtmlFile.__init__(self, filePath)
        self._lcId = None

    def handle_starttag(self, tag, attrs):
        """Identify locations.
        Overwrites HTMLparser.handle_starttag()
        """
        if tag == 'div':

            if attrs[0][0] == 'id':

                if attrs[0][1].startswith('LcID'):
                    self._lcId = re.search('[0-9]+', attrs[0][1]).group()
                    self.locations[self._lcId] = Object()

    def handle_endtag(self, tag):
        """Recognize the end of the location section and save data.
        Overwrites HTMLparser.handle_endtag().
        """
        if self._lcId is not None:

            if tag == 'div':
                self.locations[self._lcId].desc = ''.join(self._lines)
                self._lines = []
                self._lcId = None

            elif tag == 'p':
                self._lines.append('\n')

    def handle_data(self, data):
        """collect data within location sections.
        Overwrites HTMLparser.handle_data().
        """
        if self._lcId is not None:
            self._lines.append(data.rstrip().lstrip())

    def get_structure(self):
        """This file format has no comparable structure."""
