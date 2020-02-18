"""OdtFile - Class for OpenDocument xml file operations and parsing.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import zipfile

from pywriter.model.odttemplate import OdtTemplate
from pywriter.model.novel import Novel
from pywriter.model.odtform import *


class OdtFile(Novel, OdtTemplate):
    """OpenDocument xml project file representation."""
    _FILE_EXTENSION = '.odt'

    _ODT_HEADING_MARKERS = ['<text:h text:style-name="Heading_20_2" text:outline-level="2">',
                            '<text:h text:style-name="Heading_20_1" text:outline-level="1">']

    _SCENE_DIVIDER = '* * *'
    # To be placed between scene ending and beginning tags.

    def write_content_xml(self):
        """Write scene content to "content.xml".

        Considered are "used" scenes within
        chapters not marked  "Other" or "Unused" or "Info".

        Generate "content.xml" containing:
        - the scene titles as comments,
        - the scene contents.
        Return a message beginning with SUCCESS or ERROR.
        """
        lines = [self._CONTENT_XML_HEADER]

        for chId in self.srtChapters:

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

                        scenePrefix = '<text:p text:style-name="Text_20_body">'

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

        lines.append(self._CONTENT_XML_FOOTER)
        text = '\n'.join(lines)

        try:
            with open(self._TEMPDIR + '/content.xml', 'w', encoding='utf-8') as f:
                f.write(text)

        except:
            return 'ERROR: Cannot write "content.xml".'

        return 'SUCCESS: Content written to "content.xml"'

    def write(self, novel):
        """Generate an odt file from a template.
        Return a message beginning with SUCCESS or ERROR.
        """

        # Copy the novel's attributes to write

        if novel.title is None:
            self.title = ''

        else:
            self.title = novel.title

        if novel.summary is None:
            self.summary = ''

        else:
            self.summary = novel.summary

        if novel.author is None:
            self.author = ''

        else:
            self.author = novel.author

        if novel.srtChapters != []:
            self.srtChapters = novel.srtChapters

        if novel.scenes is not None:
            self.scenes = novel.scenes

        if novel.chapters is not None:
            self.chapters = novel.chapters

        message = self.set_up()

        if message.startswith('ERROR'):
            return message

        message = self.write_content_xml()

        if message.startswith('ERROR'):
            return message

        try:
            with zipfile.ZipFile(self.filePath, 'w') as odtTarget:
                workdir = os.getcwd()
                os.chdir(self._TEMPDIR)

                for file in self._ODT_COMPONENTS:
                    odtTarget.write(file)
        except:
            os.chdir(workdir)
            return 'ERROR: Cannot generate "' + self._filePath + '".'

        os.chdir(workdir)
        self.tear_down()
        return 'SUCCESS: "' + self._filePath + '" saved.'
