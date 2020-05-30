"""OdtFile - Class for OpenDocument xml file generation.

Part of the PyWriter project.
Copyright (c) 2020, peter88213
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import zipfile

from pywriter.odt.odt_template import OdtTemplate
from pywriter.model.novel import Novel
from pywriter.odt.odt_form import *


class OdtFile(Novel, OdtTemplate):
    """OpenDocument xml project file representation."""
    _FILE_EXTENSION = '.odt'

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
        lines.append(self._ODT_TITLE_START + self.title + self._ODT_PARA_END)
        lines.append(self._ODT_SUBTITLE_START +
                     self.author + self._ODT_PARA_END)

        for chId in self.srtChapters:

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

                        if self.scenes[scId].appendToPrev:
                            scenePrefix = self._ODT_PARA_START

                        else:
                            scenePrefix = self._ODT_FIRST_PARA_START

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

        lines.append(self._CONTENT_XML_FOOTER)
        text = '\n'.join(lines)

        try:
            with open(self._TEMPDIR + '/content.xml', 'w', encoding='utf-8') as f:
                f.write(text)

        except:
            return 'ERROR: Cannot write "content.xml".'

        return 'SUCCESS: Content written to "content.xml"'

    def merge(self, novel):
        """Copy selected novel attributes.
        """

        if novel.title is None:
            self.title = ''

        else:
            self.title = novel.title

        if novel.desc is None:
            self.desc = ''

        else:
            self.desc = novel.desc

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

        if novel.characters is not None:
            self.characters = novel.characters

        if novel.locations is not None:
            self.locations = novel.locations

        if novel.items is not None:
            self.items = novel.items

    def write(self):
        """Generate an odt file from a template.
        Return a message beginning with SUCCESS or ERROR.
        """

        # Create a temporary directory containing the internal
        # structure of an ODT file except "content.xml".

        message = self.set_up()

        if message.startswith('ERROR'):
            return message

        # Add "content.xml" to the temporary directory.

        message = self.write_content_xml()

        if message.startswith('ERROR'):
            return message

        # Pack the contents of the temporary directory
        # into the ODT file.

        workdir = os.getcwd()

        try:
            with zipfile.ZipFile(self.filePath, 'w') as odtTarget:
                os.chdir(self._TEMPDIR)

                for file in self._ODT_COMPONENTS:
                    odtTarget.write(file)
        except:
            os.chdir(workdir)
            return 'ERROR: Cannot generate "' + self._filePath + '".'

        # Remove temporary data.

        os.chdir(workdir)
        self.tear_down()
        return 'SUCCESS: "' + self._filePath + '" saved.'
