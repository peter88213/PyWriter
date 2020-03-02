"""OdtProofWriter - Class for OpenDocument xml file generation.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.model.odt_file_writer import OdtFileWriter
from pywriter.model.odtform import *


class OdtProofWriter(OdtFileWriter):
    """OpenDocument xml proof reading file representation."""

    _SCENE_DIVIDER = '* * *'
    # To be placed between scene ending and beginning tags.

    def write_content_xml(self):
        """Write scene content to "content.xml".

        Considered are all scenes no matter
        whether "used" or "unused".

        Generate "content.xml" containing:
        - visibly marked chapter sections containing:
            - visibly marked scene sections containing
                - the scene content.
        Return a message beginning with SUCCESS or ERROR.
        """
        lines = [self._CONTENT_XML_HEADER]
        lines.append(self._ODT_TITLE_START + self.title + self._ODT_PARA_END)
        lines.append(self._ODT_SUBTITLE_START +
                     self.author + self._ODT_PARA_END)

        for chId in self.srtChapters:

            # Write visible "start chapter" tag.

            if self.chapters[chId].isUnused:
                lines.append(
                    '<text:p text:style-name="yWriter_20_mark_20_unused">[ChID:' + chId + ' (Unused)]</text:p>')

            elif self.chapters[chId].chType != 0:
                lines.append(
                    '<text:p text:style-name="yWriter_20_mark_20_info">[ChID:' + chId + ' (Info)]</text:p>')

            else:
                lines.append(
                    '<text:p text:style-name="yWriter_20_mark">[ChID:' + chId + ']</text:p>')

            # Write chapter heading.

            lines.append(self._ODT_HEADING_STARTS[self.chapters[chId].chLevel] + format_chapter_title(
                self.chapters[chId].title) + self._ODT_HEADING_END)
            firstSceneInChapter = True

            for scId in self.chapters[chId].srtScenes:

                # Write Scene divider.

                if not firstSceneInChapter:
                    lines.append(
                        self._ODT_SCENEDIV_START + self._SCENE_DIVIDER + self._ODT_PARA_END)

                # Write visible "start scene" tag.

                if self.scenes[scId].isUnused or self.chapters[chId].isUnused:
                    lines.append(
                        '<text:p text:style-name="yWriter_20_mark_20_unused">[ScID:' + scId + ' (Unused)]</text:p>')

                elif self.chapters[chId].chType != 0:
                    lines.append(
                        '<text:p text:style-name="yWriter_20_mark_20_info">[ScID:' + scId + ' (Info)]</text:p>')

                else:
                    lines.append(
                        '<text:p text:style-name="yWriter_20_mark">[ScID:' + scId + ']</text:p>')

                # Write scene content.

                scenePrefix = self._ODT_FIRST_PARA_START

                if self.scenes[scId].sceneContent is not None:
                    lines.append(scenePrefix +
                                 to_odt(self.scenes[scId].sceneContent) + self._ODT_PARA_END)

                else:
                    lines.append(scenePrefix + self._ODT_PARA_END)

                firstSceneInChapter = False

                # Write visible "end scene" tag.

                if self.scenes[scId].isUnused or self.chapters[chId].isUnused:
                    lines.append(
                        '<text:p text:style-name="yWriter_20_mark_20_unused">[/ScID (Unused)]</text:p>')

                elif self.chapters[chId].chType != 0:
                    lines.append(
                        '<text:p text:style-name="yWriter_20_mark_20_info">[/ScID (Info)]</text:p>')

                else:
                    lines.append(
                        '<text:p text:style-name="yWriter_20_mark">[/ScID]</text:p>')

            # Write visible "end chapter" tag.

            if self.chapters[chId].isUnused:
                lines.append(
                    '<text:p text:style-name="yWriter_20_mark_20_unused">[/ChID (Unused)]</text:p>')

            elif self.chapters[chId].chType != 0:
                lines.append(
                    '<text:p text:style-name="yWriter_20_mark_20_info">[/ChID (Info)]</text:p>')

            else:
                lines.append(
                    '<text:p text:style-name="yWriter_20_mark">[/ChID]</text:p>')

        lines.append(self._CONTENT_XML_FOOTER)
        text = '\n'.join(lines)

        try:
            with open(self._TEMPDIR + '/content.xml', 'w', encoding='utf-8') as f:
                f.write(text)

        except:
            return 'ERROR: Cannot write "content.xml".'

        return 'SUCCESS: Content written to "content.xml"'
