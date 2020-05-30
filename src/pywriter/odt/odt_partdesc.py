"""OdtPartDesc - Class for OpenDocument xml file generation.

Part of the PyWriter project.
Copyright (c) 2020, peter88213
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os

from pywriter.odt.odt_file import OdtFile
from pywriter.odt.odt_form import *
from pywriter.globals import (MANUSCRIPT_ODT, PARTDESC_ODT)


class OdtPartDesc(OdtFile):
    """OpenDocument xml manuscript file representation."""

    _SCENE_DIVIDER = '* * *'
    # To be placed between scene ending and beginning tags.

    def write_content_xml(self):
        """Write part summaries to "content.xml".

        Parts are chapters marked  "Other" and not "Unused" and not "Info".

        Generate "content.xml" containing:
        - book title,
        - part sections containing:
            - the "part" (i.e. chapter) summary.
        Return a message beginning with SUCCESS or ERROR.
        """
        manuscriptPath = '../' + os.path.basename(self.filePath).replace('\\', '/').replace(
            ' ', '%20').replace(PARTDESC_ODT, MANUSCRIPT_ODT)

        lines = [self._CONTENT_XML_HEADER]
        lines.append(self._ODT_TITLE_START + self.title + self._ODT_PARA_END)
        lines.append(self._ODT_SUBTITLE_START +
                     self.author + self._ODT_PARA_END)

        for chId in self.srtChapters:

            if self.chapters[chId].chType == 0 and not self.chapters[chId].isUnused:

                if self.chapters[chId].chLevel == 1:

                    # Write chapter heading
                    # with hyperlink to manuscript.

                    lines.append(self._ODT_HEADING_STARTS[self.chapters[chId].chLevel] +
                                 '<text:a xlink:href="' +
                                 manuscriptPath + '#ChID:' + chId + '%7Cregion">' +
                                 self.chapters[chId].get_title() +
                                 '</text:a>' +
                                 self._ODT_HEADING_END)

                    # Write invisible "start chapter" tag.

                    lines.append(
                        '<text:section text:style-name="Sect1" text:name="ChID:' + chId + '">')

                    if self.chapters[chId].desc is not None:

                        # Write chapter summary.

                        lines.append(self._ODT_FIRST_PARA_START +
                                     to_odt(self.chapters[chId].desc) + self._ODT_PARA_END)

                    else:
                        lines.append(self._ODT_FIRST_PARA_START +
                                     self._ODT_PARA_END)

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
