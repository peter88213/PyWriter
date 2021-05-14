"""HtmlProof - Class for html proof reading file parsing.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import re
from pywriter.html.html_file import HtmlFile

from pywriter.model.chapter import Chapter
from pywriter.model.scene import Scene


class HtmlProof(HtmlFile):
    """HTML file representation of an yWriter project's OfficeFile part.

    Represents a html file with visible chapter and scene tags 
    to be read and written by Open/LibreOffice Writer.
    """

    DESCRIPTION = 'Tagged manuscript for proofing'
    SUFFIX = '_proof'

    def __init__(self, filePath, **kwargs):
        HtmlFile.__init__(self, filePath)
        self._collectText = False

    def preprocess(self, text):
        """Process the html text before parsing.
        """
        return self.convert_to_yw(text)

    def postprocess(self):
        """Parse the converted text to identify chapters and scenes.
        """
        sceneText = []
        scId = ''
        chId = ''
        inScene = False

        for line in self._lines:

            if '[ScID' in line:
                scId = re.search('[0-9]+', line).group()
                self.scenes[scId] = Scene()
                self.chapters[chId].srtScenes.append(scId)
                inScene = True

            elif '[/ScID' in line:
                self.scenes[scId].sceneContent = '\n'.join(sceneText)
                sceneText = []
                inScene = False

            elif '[ChID' in line:
                chId = re.search('[0-9]+', line).group()
                self.chapters[chId] = Chapter()
                self.srtChapters.append(chId)

            elif '[/ChID' in line:
                pass

            elif inScene:
                sceneText.append(line)

    def handle_starttag(self, tag, attrs):
        """Recognize the paragraph's beginning.
        Overwrites HTMLparser.handle_endtag().
        """
        if tag == 'p':
            self._collectText = True

    def handle_endtag(self, tag):
        """Recognize the paragraph's end.
        Overwrites HTMLparser.handle_endtag().
        """
        if tag == 'p':
            self._collectText = False

    def handle_data(self, data):
        """Copy the scene paragraphs.
        Overwrites HTMLparser.handle_data().
        """
        if self._collectText:
            self._lines.append(data)
