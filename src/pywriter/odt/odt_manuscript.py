"""OdtManuscript - Class for OpenDocument xml file generation.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os

from urllib.parse import quote

from pywriter.odt.odt_file import OdtFile
from pywriter.odt.odt_form import *
from pywriter.globals import *


class OdtManuscript(OdtFile):
    """OpenDocument xml manuscript file representation."""

    def write_content_xml(self):
        """Write scene content to "content.xml".

        Considered are "used" scenes within
        chapters not marked  "Other" or "Unused" or "Info".

        Generate "content.xml" containing:
        - chapter s containing:
            - scene s containing
                - the scene title as comment,
                - the scene content.
        Return a message beginning with SUCCESS or ERROR.
        """
        sceneDescPath = '../' + quote(os.path.basename(self.filePath).replace(
            '\\', '/'), '/:').replace(MANUSCRIPT_SUFFIX, SCENEDESC_SUFFIX)
        chapterDescPath = [sceneDescPath.replace(SCENEDESC_SUFFIX, CHAPTERDESC_SUFFIX),
                           sceneDescPath.replace(SCENEDESC_SUFFIX, PARTDESC_SUFFIX)]

        lines = [self._CONTENT_XML_HEADER]
        lines.append(self._ODT_TITLE_START + self.title + self._ODT_PARA_END)
        lines.append(self._ODT_SUBTITLE_START +
                     self.author + self._ODT_PARA_END)

        for chId in self.srtChapters:

            if self.chapters[chId].isUnused:
                continue

            if self.chapters[chId].chType != 0:
                continue

            # Write invisible "start chapter" tag.

            lines.append(
                '<text:section text:style-name="Sect1" text:name="ChID:' + chId + '">')

            # Write chapter heading
            # with hyperlink to chapter or part description.

            lines.append(self._ODT_HEADING_STARTS[self.chapters[chId].chLevel] +
                         '<text:a xlink:href="' +
                         chapterDescPath[self.chapters[chId].chLevel] +
                         '#ChID:' + chId + '%7Cregion">' +
                         self.chapters[chId].get_title() +
                         '</text:a>' +
                         self._ODT_HEADING_END)

            firstSceneInChapter = True

            for scId in self.chapters[chId].srtScenes:

                if self.scenes[scId].isUnused:
                    continue

                if self.scenes[scId].doNotExport:
                    continue

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

                # Write scene title as comment.

                scenePrefix += ('<office:annotation>\n' +
                                '<dc:creator>scene title</dc:creator>\n' +
                                '<text:p>' + self.scenes[scId].title + '</text:p>\n' +
                                '<text:p/>\n' +
                                '<text:p><text:a xlink:href="' +
                                sceneDescPath + '#ScID:' +
                                scId + '%7Cregion">→Summary</text:a></text:p>\n' +
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
