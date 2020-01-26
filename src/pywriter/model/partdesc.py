"""PartDesc - Class for part desc. file operations and parsing.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from pywriter.model.novel import Novel
from pywriter.model.chapter import Chapter
from pywriter.model.chapterdesc import ChapterDesc
from pywriter.model.hform import *


class PartDesc(ChapterDesc):
    """HTML file representation of an yWriter project's chapter descriptions part.

    Represents a html file with chapter sections containing chapter 
    descriptions to be read and written by Open/LibreOffice Writer.

    # Methods

    write : str
        Arguments 
            novel : Novel
                the data to be written. 
        Generate a html file containing:
        - book title,
        - chapter sections containing:
            - chapter description.
        Return a message beginning with SUCCESS or ERROR.
    """

    def write(self, novel: Novel) -> str:
        """Write novel attributes to html file. """

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
                    lines.append('<div id="ChID:' + chId + '">\n')
                    lines.append('<p class="firstlineindent">')

                    try:
                        entry = self.chapters[chId].desc

                        if entry == '':
                            entry = self.chapters[chId].title

                        else:
                            entry = to_html(entry)

                        lines.append(entry)

                    except(KeyError):
                        pass

                    lines.append('</p>\n')
                    lines.append('</div>\n')

        lines.append(HTML_FOOTER)

        try:
            with open(self._filePath, 'w', encoding='utf-8') as f:
                f.writelines(lines)

        except(PermissionError):
            return 'ERROR: ' + self._filePath + '" is write protected.'

        return 'SUCCESS: "' + self._filePath + '" saved.'
