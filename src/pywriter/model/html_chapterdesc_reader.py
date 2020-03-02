"""HtmlChapterDescReader - Class for html chapter summary file parsing.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from pywriter.model.html_scenedesc_reader import HtmlSceneDescReader


class HtmlChapterDescReader(HtmlSceneDescReader):
    """HTML file representation of an yWriter project's chapters summaries."""

    def handle_endtag(self, tag):
        """Recognize the end of the chapter section and save data.
        Overwrites HTMLparser.handle_endtag().
        """
        if self._chId is not None:

            if tag == 'div':
                self.chapters[self._chId].summary = ''.join(self._lines)
                self._lines = []
                self._chId = None

            elif tag == 'p':
                self._lines.append('\n')

    def handle_data(self, data):
        """collect data within chapter sections.
        Overwrites HTMLparser.handle_data().
        """
        if self._chId is not None:
            self._lines.append(data.rstrip().lstrip())
