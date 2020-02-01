"""ChapterDesc - Class for chapter summary. file operations and parsing.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from pywriter.model.novel import Novel
from pywriter.model.scenedesc import SceneDesc
from pywriter.model.hform import *


class ChapterDesc(SceneDesc):
    """HTML file representation of an yWriter project's chapters summaries.
    """

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

    def write(self, novel: Novel) -> str:
        """Write chapter summaries to a html file.

        Chapters are chapters marked "Chapter".
        Generate a html file containing:
        - book title,
        - chapter sections containing:
            - chapter summary.
        Return a message beginning with SUCCESS or ERROR.
        """

        def to_html(text: str) -> str:
            """Convert yw7 raw markup """
            try:
                text = text.replace('\n\n', '\n')
                text = text.replace('\n', '</p>\n<p class="firstlineindent">')

            except:
                pass

            return text

        # Copy the novel's attributes to write

        if novel.title is not None:

            if novel.title != '':
                self.title = novel.title

        if novel.srtChapters != []:
            self.srtChapters = novel.srtChapters

        if novel.chapters is not None:
            self.chapters = novel.chapters

        lines = [HTML_HEADER.replace('$bookTitle$', self.title)]
        lines.append('<h1>' + self.title + '</h1>\n')

        for chId in self.srtChapters:

            if (not self.chapters[chId].isUnused) and self.chapters[chId].chType == 0:

                if self.chapters[chId].chLevel != 0:
                    lines.append(
                        '<h2>' + self.chapters[chId].title + '</h2>\n')

                else:
                    lines.append('<div id="ChID:' + chId + '">\n')
                    lines.append('<p class="firstlineindent">')

                    if self.chapters[chId].summary is not None:
                        lines.append(to_html(self.chapters[chId].summary))

                    else:
                        lines.append(
                            '<!-- ' + self.chapters[chId].title + ' -->')

                    lines.append('</p>\n')
                    lines.append('</div>\n')

        lines.append(HTML_FOOTER)

        try:
            with open(self._filePath, 'w', encoding='utf-8') as f:
                f.writelines(lines)

        except(PermissionError):
            return 'ERROR: ' + self._filePath + '" is write protected.'

        return 'SUCCESS: "' + self._filePath + '" saved.'
