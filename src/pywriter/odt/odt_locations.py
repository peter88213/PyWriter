"""OdtLocations - Class for OpenDocument xml file generation.

Part of the PyWriter project.
Copyright (c) 2020, peter88213
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os

from pywriter.odt.odt_file import OdtFile
from pywriter.odt.odt_form import *


class OdtLocations(OdtFile):
    """OpenDocument xml location descriptions file representation."""

    def write_content_xml(self):
        """Write location descriptions to "content.xml".


        Generate "content.xml" containing:
        - book title,
        - location sections containing:
            - the location description.
        Return a message beginning with SUCCESS or ERROR.
        """
        manuscriptPath = '../' + os.path.basename(self.filePath).replace('\\', '/').replace(
            ' ', '%20').replace(self._CHAPTERDESC_SUFFIX, self._MANUSCRIPT_SUFFIX)
        partDescPath = manuscriptPath.replace(
            self._MANUSCRIPT_SUFFIX, self._PARTDESC_SUFFIX)
        linkPath = [manuscriptPath, partDescPath]

        lines = [self._CONTENT_XML_HEADER]
        lines.append(self._ODT_TITLE_START + self.title +
                     self._ODT_PARA_END)
        lines.append(self._ODT_SUBTITLE_START +
                     'Locations' + self._ODT_PARA_END)

        for lcId in self.locations:

            # Write location title as heading

            if self.locations[lcId].aka:
                aka = ' ("' + self.locations[lcId].aka + '")'

            else:
                aka = ''

            lines.append(
                self._ODT_HEADING_STARTS[0] + self.locations[lcId].title + aka + self._ODT_HEADING_END)

            # Write invisible "start location" tag.

            lines.append(
                '<text:section text:style-name="Sect1" text:name="LcID:' + lcId + '">')


            if self.locations[lcId].desc is not None:

                # Write location description.

                lines.append(self._ODT_FIRST_PARA_START +
                             to_odt(self.locations[lcId].desc) + self._ODT_PARA_END)

            else:
                lines.append(self._ODT_FIRST_PARA_START + self._ODT_PARA_END)

            # Write invisible "end location" tag.

            lines.append('</text:section>')

        lines.append(self._CONTENT_XML_FOOTER)
        text = '\n'.join(lines)

        try:
            with open(self._TEMPDIR + '/content.xml', 'w', encoding='utf-8') as f:
                f.write(text)

        except:
            return 'ERROR: Cannot write "content.xml".'

        return 'SUCCESS: Content written to "content.xml"'
