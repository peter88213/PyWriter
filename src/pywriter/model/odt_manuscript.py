"""OdtManuscript - Class for OpenDocument xml file operations and parsing.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.model.odtfile import OdtFile
from pywriter.model.odtform import *


class OdtManuscript(OdtFile):
    """OpenDocument xml manuscript file representation."""

    _ODT_HEADING_MARKERS = ['<text:h text:style-name="Heading_20_2" text:outline-level="2">',
                            '<text:h text:style-name="Heading_20_1" text:outline-level="1">']

    _SCENE_DIVIDER = '* * *'
    # To be placed between scene ending and beginning tags.

    def write_content_xml(self):
        """Write scene content to "content.xml".

        Considered are "used" scenes within
        chapters not marked  "Other" or "Unused" or "Info".

        Generate "content.xml" containing:
        - chapter sections containing:
            - scene sections containing
                - a navigable bookmark,
                - the scene title as comment,
                - the scene content.
        Return a message beginning with SUCCESS or ERROR.
        """
        lines = [self._CONTENT_XML_HEADER]

        for chId in self.srtChapters:

            # Write invisible "start chapter" tag.

            if self.chapters[chId].chType == 0 and not self.chapters[chId].isUnused:
                lines.append(
                    '<text:section text:style-name="Sect1" text:name="ChID:' + chId + '">')

            if (not self.chapters[chId].isUnused) and self.chapters[chId].chType == 0:

                # Write chapter heading.

                headingMarker = self._ODT_HEADING_MARKERS[self.chapters[chId].chLevel]
                lines.append(headingMarker + format_chapter_title(
                    self.chapters[chId].title) + '</text:h>')

                firstSceneInChapter = True

                for scId in self.chapters[chId].srtScenes:

                    if not self.scenes[scId].isUnused:

                        # Write Scene divider.

                        if not firstSceneInChapter:
                            lines.append(
                                '<text:p text:style-name="Heading_20_4">' + self._SCENE_DIVIDER + '</text:p>')

                        # Write invisible "start scene" tag.

                        lines.append(
                            '<text:section text:style-name="Sect1" text:name="ScID:' + scId + '">')

                        scenePrefix = '<text:p text:style-name="Text_20_body">'

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
                                         to_odt(self.scenes[scId].sceneContent) + '</text:p>')

                        else:
                            lines.append(scenePrefix + '</text:p>')

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
