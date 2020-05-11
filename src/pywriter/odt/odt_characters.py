"""OdtCharacters - Class for OpenDocument xml file generation.

Part of the PyWriter project.
Copyright (c) 2020, peter88213
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os

from pywriter.odt.odt_file import OdtFile
from pywriter.odt.odt_form import *


class OdtCharacters(OdtFile):
    """OpenDocument xml character descriptions file representation."""

    def write_content_xml(self):
        """Write character descriptions to "content.xml".


        Generate "content.xml" containing:
        - book title,
        - character sections containing:
            - the character description.
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
                     'Characters' + self._ODT_PARA_END)


        for crId in self.characters:

            # Write character title as heading

            if self.characters[crId].aka:
                aka = ' ("' + self.characters[crId].aka + '")'

            else:
                aka = ''

            if self.characters[crId].fullName:
                fullName = '/' + self.characters[crId].fullName

            else:
                fullName = ''

            lines.append(
                self._ODT_HEADING_STARTS[0] + self.characters[crId].title + fullName + aka + self._ODT_HEADING_END)

            lines.append(
                self._ODT_HEADING_STARTS[2] + 'Description' + self._ODT_HEADING_END)

            # Write invisible "start character description" tag.

            lines.append(
                '<text:section text:style-name="Sect1" text:name="CrID_desc:' + crId + '">')

            if self.characters[crId].desc is not None:

                # Write character description.

                lines.append(self._ODT_FIRST_PARA_START +
                             to_odt(self.characters[crId].desc) + self._ODT_PARA_END)

            else:
                lines.append(self._ODT_FIRST_PARA_START + self._ODT_PARA_END)

            # Write invisible "end character description" tag.

            lines.append('</text:section>')

            lines.append(
                self._ODT_HEADING_STARTS[2] + 'Bio' + self._ODT_HEADING_END)

            # Write invisible "start character bio" tag.

            lines.append(
                '<text:section text:style-name="Sect1" text:name="CrID_bio:' + crId + '">')

            if self.characters[crId].bio is not None:

                # Write character bio.

                lines.append(self._ODT_FIRST_PARA_START +
                             to_odt(self.characters[crId].bio) + self._ODT_PARA_END)

            else:
                lines.append(self._ODT_FIRST_PARA_START + self._ODT_PARA_END)

            # Write invisible "end character bio" tag.

            lines.append('</text:section>')

            lines.append(
                self._ODT_HEADING_STARTS[2] + 'Goals' + self._ODT_HEADING_END)

            # Write invisible "start character goals" tag.

            lines.append(
                '<text:section text:style-name="Sect1" text:name="CrID_goals:' + crId + '">')

            if self.characters[crId].goals is not None:

                # Write character goals.

                lines.append(self._ODT_FIRST_PARA_START +
                             to_odt(self.characters[crId].goals) + self._ODT_PARA_END)

            else:
                lines.append(self._ODT_FIRST_PARA_START + self._ODT_PARA_END)

            # Write invisible "end character goals" tag.

            lines.append('</text:section>')

        lines.append(self._CONTENT_XML_FOOTER)
        text = '\n'.join(lines)

        try:
            with open(self._TEMPDIR + '/content.xml', 'w', encoding='utf-8') as f:
                f.write(text)

        except:
            return 'ERROR: Cannot write "content.xml".'

        return 'SUCCESS: Content written to "content.xml"'
