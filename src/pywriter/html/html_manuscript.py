"""Provide a class for html invisibly tagged chapters and scenes import.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from pywriter.html.html_file import HtmlFile


class HtmlManuscript(HtmlFile):
    """HTML manuscript file representation.

    Import a manuscript with invisibly tagged chapters and scenes.
    """

    DESCRIPTION = 'Editable manuscript'
    SUFFIX = '_manuscript'

    def preprocess(self, text):
        """Process the html text before parsing.
        """
        return self.convert_to_yw(text)

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
        Override HTMLparser.handle_data().
        """
        if self._scId is not None:
            self._lines.append(data.rstrip().lstrip())

        elif self._chId is not None:

            if not self.chapters[self._chId].title:
                self.chapters[self._chId].title = data.rstrip().lstrip()
