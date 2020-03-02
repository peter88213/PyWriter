"""HtmlSceneDescWriter - Class for html scene summary file generation.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from pywriter.model.novel import Novel
from pywriter.model.hform import *


class HtmlSceneDescWriter(Novel):
    """HTML file representation of an yWriter project's scene summaries."""

    _FILE_EXTENSION = 'html'
    # overwrites Novel._FILE_EXTENSION

    _HTML_HEADING_MARKERS = ("h3", "h2")
    # Index is yWriter's chapter chLevel:
    # 0 is for an ordinary chapter
    # 1 is for a chapter beginning a section

    def write(self, novel):
        """Generate a html file containing:
        - chapter sections containing:
            - chapter headings,
            - scene sections containing:
                - scene ID as anchor,
                - scene title as comment,
                - scene summary.
        Return a message beginning with SUCCESS or ERROR.
        """

        def format_chapter_title(text):
            """Fix auto-chapter titles for non-English """
            text = text.replace('Chapter ', '')
            return text

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

        if novel.scenes is not None:
            self.scenes = novel.scenes

        if novel.chapters is not None:
            self.chapters = novel.chapters

        lines = [HTML_HEADER.replace('$bookTitle$', self.title)]
        lines.append('<h1>' + self.title + '</h1>')

        for chId in self.srtChapters:

            if (not self.chapters[chId].isUnused) and self.chapters[chId].chType == 0:
                lines.append('<div id="ChID:' + chId + '">\n')
                headingMarker = self._HTML_HEADING_MARKERS[self.chapters[chId].chLevel]
                lines.append('<' + headingMarker + '>' + format_chapter_title(
                    self.chapters[chId].title) + '</' + headingMarker + '>\n')

                for scId in self.chapters[chId].srtScenes:

                    if not self.scenes[scId].isUnused:
                        lines.append('<div id="ScID:' + scId + '">\n')
                        lines.append('<p class="firstlineindent">')

                        # Insert scene ID as anchor.

                        lines.append('<a name="ScID:' + scId + '" />')

                        # Insert scene title as comment.

                        lines.append(
                            '<!-- ' + self.scenes[scId].title + ' -->\n')

                        if self.scenes[scId].summary is not None:
                            lines.append(to_html(self.scenes[scId].summary))

                        lines.append('</p>\n')
                        lines.append('</div>\n')

                lines.append('</div>\n')

        lines.append(HTML_FOOTER)

        try:
            with open(self._filePath, 'w', encoding='utf-8') as f:
                f.writelines(lines)

        except(PermissionError):
            return 'ERROR: ' + self._filePath + '" is write protected.'

        return 'SUCCESS: "' + self._filePath + '" saved.'
