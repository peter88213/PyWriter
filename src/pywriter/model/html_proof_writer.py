"""HtmlProofWriter - Class for html file generation.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from pywriter.model.novel import Novel
from pywriter.model.hform import *


class HtmlProofWriter(Novel):
    """HTML file representation of an yWriter project's OfficeFile part.

    Represents a html file with visible chapter and scene tags 
    to be read and written by Open/LibreOffice Writer.
    """

    _HTML_HEADING_MARKERS = ("h2", "h1")
    # Index is yWriter's chapter chLevel:
    # 0 is for an ordinary chapter
    # 1 is for a chapter beginning a section

    _FILE_EXTENSION = 'html'
    # overwrites Novel._FILE_EXTENSION

    def write(self, novel):
        """Generate a html file containing:
        - chapter ID tags,
        - chapter headings,
        - scene ID tags, 
        - scene content.
        Return a message beginning with SUCCESS or ERROR.
        """

        def format_chapter_title(text):
            """Fix auto-chapter titles for non-English """
            text = text.replace('Chapter ', '')
            return text

        # Copy the novel's attributes to write

        if novel.title is not None:

            if novel.title is not None:
                self.title = novel.title

        if novel.srtChapters != []:
            self.srtChapters = novel.srtChapters

        self.scenes = novel.scenes
        self.chapters = novel.chapters
        lines = [HTML_HEADER.replace('$bookTitle$', self.title)]

        for chId in self.srtChapters:

            if self.chapters[chId].isUnused:
                lines.append(
                    '<p style="font-size:x-small">[ChID:' + chId + ' (Unused)]</p>')

            else:
                lines.append(
                    '<p style="font-size:x-small">[ChID:' + chId + ']</p>')

            headingMarker = self._HTML_HEADING_MARKERS[self.chapters[chId].chLevel]
            lines.append('<' + headingMarker + '>' + format_chapter_title(
                self.chapters[chId].title) + '</' + headingMarker + '>')

            for scId in self.chapters[chId].srtScenes:
                lines.append('<h4>' + HTML_SCENE_DIVIDER + '</h4>')

                if self.scenes[scId].isUnused:
                    lines.append(
                        '<p style="font-size:x-small">[ScID:' + scId + ' (Unused)]</p>')

                else:
                    lines.append(
                        '<p style="font-size:x-small">[ScID:' + scId + ']</p>')

                if self.scenes[scId].sceneContent is not None:
                    lines.append('<p class="textbody">' +
                                 to_html(self.scenes[scId].sceneContent) + '</p>')

                if self.scenes[scId].isUnused:
                    lines.append(
                        '<p style="font-size:x-small">[/ScID (Unused)]</p>')

                else:
                    lines.append('<p style="font-size:x-small">[/ScID]</p>')

            if self.chapters[chId].isUnused:
                lines.append(
                    '<p style="font-size:x-small">[/ChID (Unused)]</p>')

            else:
                lines.append('<p style="font-size:x-small">[/ChID]</p>')

        lines.append(HTML_FOOTER)
        text = '\n'.join(lines)

        # Remove scene dividers from chapter's beginning

        text = text.replace(
            '</h1>\n<h4>' + HTML_SCENE_DIVIDER + '</h4>', '</h1>')
        text = text.replace(
            '</h2>\n<h4>' + HTML_SCENE_DIVIDER + '</h4>', '</h2>')

        try:
            with open(self._filePath, 'w', encoding='utf-8') as f:
                f.write(text)

        except(PermissionError):
            return 'ERROR: ' + self._filePath + '" is write protected.'

        return 'SUCCESS: "' + self._filePath + '" saved.'
