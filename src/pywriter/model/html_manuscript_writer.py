"""HtmlManuscriptWriter - Class for html manuscript file generation.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from pywriter.model.novel import Novel
from pywriter.model.hform import *


class HtmlManuscriptWriter(Novel):
    """HTML file representation of an yWriter project's manuscript part.

    Represents a html file with chapter and scene sections 
    containing scene contents to be read and written by 
    OpenOffice/LibreOffice Writer.
    """

    _FILE_EXTENSION = 'html'
    # overwrites Novel._FILE_EXTENSION

    _HTML_HEADING_MARKERS = ("h2", "h1")
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
                - scene content.
        Return a message beginning with SUCCESS or ERROR.
        """

        def format_chapter_title(text):
            """Fix auto-chapter titles for non-English """
            text = text.replace('Chapter ', '')
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

        for chId in self.srtChapters:

            if (not self.chapters[chId].isUnused) and self.chapters[chId].chType == 0:
                lines.append('<div id="ChID:' + chId + '">')
                headingMarker = self._HTML_HEADING_MARKERS[self.chapters[chId].chLevel]
                lines.append('<' + headingMarker + '>' + format_chapter_title(
                    self.chapters[chId].title) + '</' + headingMarker + '>')

                for scId in self.chapters[chId].srtScenes:

                    if not self.scenes[scId].isUnused:
                        lines.append('<h4>' + HTML_SCENE_DIVIDER + '</h4>')
                        lines.append('<div id="ScID:' + scId + '">')
                        lines.append('<p class="textbody">')

                        # Insert scene ID as anchor.

                        lines.append('<a name="ScID:' + scId + '" />')

                        # Insert scene title as comment.

                        lines.append(
                            '<!-- ' + self.scenes[scId].title + ' -->')

                        if self.scenes[scId].sceneContent is not None:
                            lines.append(
                                to_html(self.scenes[scId].sceneContent))

                        lines.append('</p>')
                        lines.append('</div>')

                lines.append('</div>')

        lines.append(HTML_FOOTER)
        text = '\n'.join(lines)

        # Remove scene dividers from chapter's beginning

        text = text.replace('</h1>\n<h4>' + HTML_SCENE_DIVIDER + '</h4>',
                            '</h1>')
        text = text.replace('</h2>\n<h4>' + HTML_SCENE_DIVIDER + '</h4>',
                            '</h2>')

        try:
            with open(self._filePath, 'w', encoding='utf-8') as f:
                f.write(text)

        except(PermissionError):
            return 'ERROR: ' + self._filePath + '" is write protected.'

        return 'SUCCESS: "' + self._filePath + '" saved.'

    def get_structure(self):
        """This file format has no comparable structure."""
        return None
