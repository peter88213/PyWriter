"""OdtFile - Class for OpenDocument xml file operations and parsing.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import zipfile
from abc import abstractmethod

from pywriter.model.odttemplate import OdtTemplate
from pywriter.model.novel import Novel


class OdtFile(Novel, OdtTemplate):
    """OpenDocument xml project file representation."""
    _FILE_EXTENSION = '.odt'

    @abstractmethod
    def write_content_xml(self):
        """Generate "content.xml".
        To be overwritten by file format specific subclasses.
        """

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
