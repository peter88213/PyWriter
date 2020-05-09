"""OdtChapterDesc - Class for OpenDocument xml file generation.

Part of the PyWriter project.
Copyright (c) 2020, peter88213
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os

from pywriter.odt.odt_file import OdtFile
from pywriter.odt.odt_form import *


class OdtChapterDesc(OdtFile):
    """OpenDocument xml manuscript file representation."""

    _SCENE_DIVIDER = '* * *'
    # To be placed between scene ending and beginning tags.

    def write_content_xml(self):
        """Write chapter summaries to "content.xml".

        Considered are chapters not marked  "Other" or "Unused" or "Info".

        Generate "content.xml" containing:
        - book title,
        - chapter sections containing:
            - the chapter summary.
        Return a message beginning with SUCCESS or ERROR.
        """
        manuscriptPath = '../' + os.path.basename(self.filePath).replace('\\', '/').replace(
            ' ', '%20').replace(self._CHAPTERDESC_SUFFIX, self._MANUSCRIPT_SUFFIX)
        partDescPath = manuscriptPath.replace(
            self._MANUSCRIPT_SUFFIX, self._PARTDESC_SUFFIX)
        linkPath = [manuscriptPath, partDescPath]

        lines = [self._CONTENT_XML_HEADER]
        lines.append(self._ODT_TITLE_START + self.title + self._ODT_PARA_END)
        lines.append(self._ODT_SUBTITLE_START +
                     self.author + self._ODT_PARA_END)

        for chId in self.srtChapters:

            if self.chapters[chId].chType == 0 and not self.chapters[chId].isUnused:

                # Write chapter heading
                # with hyperlink to manuscript or part description.

                lines.append(self._ODT_HEADING_STARTS[self.chapters[chId].chLevel] +
                             '<text:a xlink:href="' +
                             linkPath[self.chapters[chId].chLevel] +
                             '#ChID:' + chId + '%7Cregion">' +
                             self.chapters[chId].get_title() +
                             '</text:a>' +
                             self._ODT_HEADING_END)

                if self.chapters[chId].chLevel == 0:

                    # Write invisible "start chapter" tag.

                    lines.append(
                        '<text:section text:style-name="Sect1" text:name="ChID:' + chId + '">')

                    chapterPrefix = self._ODT_FIRST_PARA_START

                    if self.chapters[chId].desc is not None:

                        # Write chapter summary.

                        lines.append(chapterPrefix +
                                     to_odt(self.chapters[chId].desc) + self._ODT_PARA_END)

                    else:
                        lines.append(chapterPrefix + self._ODT_PARA_END)

                    # Write invisible "end chapter" tag.

                    lines.append('</text:section>')

        lines.append(self._CONTENT_XML_FOOTER)
        text = '\n'.join(lines)

        try:
            with open(self._TEMPDIR + '/content.xml', 'w', encoding='utf-8') as f:
                f.write(text)

        except:
            return 'ERROR: Cannot write "content.xml".'

        return 'SUCCESS: Content written to "content.xml"'
