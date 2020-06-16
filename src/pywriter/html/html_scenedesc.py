"""HtmlSceneDesc - Class for html scene summary file parsing.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from pywriter.html.html_manuscript import HtmlManuscript
from pywriter.html.html_form import *


class HtmlSceneDesc(HtmlManuscript):
    """HTML file representation of an yWriter project's scene summaries."""

    def handle_endtag(self, tag):
        """Recognize the end of the scene section and save data.
        Overwrites HTMLparser.handle_endtag().
        """
        if self._scId is not None:

            if tag == 'div':
                self.scenes[self._scId].desc = ''.join(self._lines)
                self._lines = []
                self._scId = None

            elif tag == 'p':
                self._lines.append('\n')

        elif self._chId is not None:

            if tag == 'div':
                self._chId = None

    def read(self):
        """Read scene summaries from a html file 
        with chapter and scene sections.
        Return a message beginning with SUCCESS or ERROR. 
        """
        result = read_html_file(self._filePath)

        if result[0].startswith('ERROR'):
            return (result[0])

        text = strip_markup(to_yw7(result[1]))

        # Invoke HTML parser.

        self.feed(text)
        return 'SUCCESS: ' + str(len(self.scenes)) + ' Scenes read from "' + self._filePath + '".'
