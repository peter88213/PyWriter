"""OdtBookDescWriter - Class for OpenDocument xml file generation.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import zipfile

from pywriter.model.odttemplate import OdtTemplate
from pywriter.model.odtform import *
from pywriter.collection.series import Series
from pywriter.collection.collection import Collection


class OdtBookDescWriter(OdtTemplate):
    """OpenDocument xml file representation of a book series containing
    a series summary and the series' book summaries 
    """
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

    def write(self, series: Series, collection):
        """Generate an odt file containing:
        - A series sections containing:
            - series title heading,
            - series summary,
            - book sections containing:
                - book title heading,
                - book summary.
        Return a message beginning with SUCCESS or ERROR.
        """

        message = self.set_up()

        if message.startswith('ERROR'):
            return message

        message = self.write_content_xml()

        if message.startswith('ERROR'):
            return message

        workdir = os.getcwd()

        try:
            with zipfile.ZipFile(self.filePath, 'w') as odtTarget:
                os.chdir(self._TEMPDIR)

                for file in self._ODT_COMPONENTS:
                    odtTarget.write(file)
        except:
            os.chdir(workdir)
            return 'ERROR: Cannot generate "' + self._filePath + '".'

        os.chdir(workdir)
        self.tear_down()
        return 'SUCCESS: "' + self._filePath + '" saved.'
