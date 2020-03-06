"""OdtManuscriptWriter - Class for OpenDocument xml file generation.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.model.odt_file_writer import OdtFileWriter
from pywriter.model.odtform import *


class OdtManuscriptWriter(OdtFileWriter):
    """OpenDocument xml manuscript file representation."""

    def write_content_xml(self):
        """Write scene content to "content.xml".

        Considered are "used" scenes within
        chapters not marked  "Other" or "Unused" or "Info".

        Generate "content.xml" containing:
        - chapter s containing:
            - scene s containing
                - a navigable bookmark,
                - the scene title as comment,
                - the scene content.
        Return a message beginning with SUCCESS or ERROR.
        """
        lines = [self._CONTENT_XML_HEADER]
        lines.append(self._ODT_TITLE_START + self.title + self._ODT_PARA_END)
        lines.append(self._ODT_SUBTITLE_START +
                     self.author + self._ODT_PARA_END)

        for chId in self.srtChapters:

            # Write invisible "start chapter" tag.

            if self.chapters[chId].chType == 0 and not self.chapters[chId].isUnused:
                lines.append(
                    '<text:section text:style-name="Sect1" text:name="ChID:' + chId + '">')

            if (not self.chapters[chId].isUnused) and self.chapters[chId].chType == 0:

                # Write chapter heading.

                lines.append(self._ODT_HEADING_STARTS[self.chapters[chId].chLevel] +
                             self.chapters[chId].get_title() + self._ODT_HEADING_END)
                firstSceneInChapter = True

                for scId in self.chapters[chId].srtScenes:

                    if not self.scenes[scId].isUnused:

                        # Write Scene divider.

                        if not (firstSceneInChapter or self.scenes[scId].appendToPrev):
                            lines.append(
                                self._ODT_SCENEDIV_START + self._SCENE_DIVIDER + self._ODT_PARA_END)

                        # Write invisible "start scene" tag.

                        lines.append(
                            '<text:section text:style-name="Sect1" text:name="ScID:' + scId + '">')

                        if self.scenes[scId].appendToPrev:
                            scenePrefix = self._ODT_PARA_START

                        else:
                            scenePrefix = self._ODT_FIRST_PARA_START

                        # Write navigable bookmark.

                        scenePrefix += '<text:bookmark text:name="ScID:' + scId + '"/>'

                        # Write scene title as comment.

                        scenePrefix += ('<office:annotation>\n' +
                                        '<dc:creator>scene title</dc:creator>\n' +
                                        '<text:p>' + self.scenes[scId].title + '</text:p>\n' +
                                        '</office:annotation>')

                        # Write scene content.

                        if self.scenes[scId].sceneContent is not None:
                            lines.append(scenePrefix +
                                         to_odt(self.scenes[scId].sceneContent) + self._ODT_PARA_END)

                        else:
                            lines.append(scenePrefix + self._ODT_PARA_END)

                        firstSceneInChapter = False

                        # Write invisible "end scene" tag.

                        lines.append('</text:section>')

            if self.chapters[chId].chType == 0 and not self.chapters[chId].isUnused:

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
