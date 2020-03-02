"""HtmlChapterDescWriter - Class for html chapter summary file generation.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from pywriter.model.novel import Novel
from pywriter.model.hform import *


class HtmlChapterDescWriter(Novel):
    """HTML file representation of an yWriter project's chapters summaries."""

    _FILE_EXTENSION = 'html'
    # overwrites Novel._FILE_EXTENSION

    def write(self, novel):
        """Write chapter summaries to a html file.

        Chapters are chapters marked "Chapter".
        Generate a html file containing:
        - book title,
        - chapter sections containing:
            - chapter summary.
        Return a message beginning with SUCCESS or ERROR.
        """

        def to_html(text):
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

                if self.chapters[chId].chLevel == 1:

                    # Write part heading.

                    lines.append(
                        '<h2>' + self.chapters[chId].title + '</h2>\n')

                else:
                    # Write invisible "start chapter" tag.

                    lines.append('<div id="ChID:' + chId + '">\n')
                    lines.append('<p class="firstlineindent">')

                    if self.chapters[chId].summary is not None:

                        # Write chapter summary.

                        lines.append(to_html(self.chapters[chId].summary))

                    else:
                        # Write chapter title as comment.

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
