"""OdtChapterDescWriter - Class for OpenDocument xml file generation.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os

from pywriter.model.odt_file_writer import OdtFileWriter
from pywriter.model.odtform import *


class OdtChapterDescWriter(OdtFileWriter):
    """OpenDocument xml manuscript file representation."""

    _SCENE_DIVIDER = '* * *'
    # To be placed between scene ending and beginning tags.

    _CHAPTERDESC_SUFFIX = '_chapters.odt'
    _MANUSCRIPT_SUFFIX = '_manuscript.odt'

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

        lines = [self._CONTENT_XML_HEADER]
        lines.append(self._ODT_TITLE_START + self.title + self._ODT_PARA_END)
        lines.append(self._ODT_SUBTITLE_START +
                     self.author + self._ODT_PARA_END)

        for chId in self.srtChapters:

            if self.chapters[chId].chType == 0 and not self.chapters[chId].isUnused:

                # Write chapter heading with navigable bookmark
                # and hyperlink to manuscript.

                lines.append(self._ODT_HEADING_STARTS[self.chapters[chId].chLevel] +
                             '<text:bookmark text:name="ChID:' + chId + '"/>' +
                             '<text:a xlink:href="' +
                             manuscriptPath + '#ChID:' + chId + '">' +
                             self.chapters[chId].get_title() +
                             '</text:a>' +
                             self._ODT_HEADING_END)

                if self.chapters[chId].chLevel == 0:

                    # Write invisible "start chapter" tag.

                    lines.append(
                        '<text:section text:style-name="Sect1" text:name="ChID:' + chId + '">')

                    chapterPrefix = self._ODT_FIRST_PARA_START

                    if self.chapters[chId].summary is not None:

                        # Write chapter summary.

                        lines.append(chapterPrefix +
                                     to_odt(self.chapters[chId].summary) + self._ODT_PARA_END)

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
