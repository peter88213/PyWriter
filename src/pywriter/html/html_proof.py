"""Provide a class for html visibly tagged chapters and scenes import.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import re
from pywriter.html.html_file import HtmlFile

from pywriter.model.chapter import Chapter
from pywriter.model.scene import Scene
from pywriter.model.splitter import Splitter


class HtmlProof(HtmlFile):
    """HTML proof reading file representation.

    Import a manuscript with visibly tagged chapters and scenes.
    """

    DESCRIPTION = 'Tagged manuscript for proofing'
    SUFFIX = '_proof'

    def __init__(self, filePath, **kwargs):
        super().__init__(filePath)
        self._prefix = None

    def _preprocess(self, text):
        """Process the html text before parsing.
        """
        return self._convert_to_yw(text)

    def _postprocess(self):
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
            self._prefix = ''

        elif tag == 'h2':
            self._prefix = Splitter.CHAPTER_SEPARATOR

        elif tag == 'h1':
            self._prefix = Splitter.PART_SEPARATOR

    def handle_endtag(self, tag):
        """Recognize the paragraph's end.
        Overwrites HTMLparser.handle_endtag().
        """
        if tag in ['p', 'h2', 'h1']:
            self._prefix = None

    def handle_data(self, data):
        """Copy the scene paragraphs.
        Overwrites HTMLparser.handle_data().
        """
        if self._prefix is not None:
            self._lines.append(f'{self._prefix}{data}')
