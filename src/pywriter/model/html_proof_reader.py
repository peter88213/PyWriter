"""HtmlProofReader - Class for html proof reading file parsing.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from html.parser import HTMLParser

from pywriter.model.novel import Novel
from pywriter.model.chapter import Chapter
from pywriter.model.scene import Scene
from pywriter.model.hform import *


class HtmlProofReader(Novel, HTMLParser):
    """HTML file representation of an yWriter project's OfficeFile part.

    Represents a html file with visible chapter and scene tags 
    to be read and written by Open/LibreOffice Writer.
    """

    _FILE_EXTENSION = 'html'
    # overwrites Novel._FILE_EXTENSION

    def __init__(self, filePath):
        Novel.__init__(self, filePath)
        HTMLParser.__init__(self)
        self._lines = []
        self._collectText = False

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

    def read(self):
        """Read scene content from a html file  
        with visible chapter and scene tags.
        Return a message beginning with SUCCESS or ERROR.
        """
        result = read_html_file(self._filePath)

        if result[0].startswith('ERROR'):
            return (result[0])

        text = to_yw7(result[1])

        # Invoke HTML parser to write the html body as raw text
        # to self._lines.

        self.feed(text)

        # Parse the HTML body to identify chapters and scenes.

        sceneText = []
        scId = ''
        chId = ''
        inScene = False

        for line in self._lines:

            if line.startswith('[ScID'):
                scId = re.search('[0-9]+', line).group()
                self.scenes[scId] = Scene()
                self.chapters[chId].srtScenes.append(scId)
                inScene = True

            elif line.startswith('[/ScID'):
                self.scenes[scId].sceneContent = '\n'.join(sceneText)
                sceneText = []
                inScene = False

            elif line.startswith('[ChID'):
                chId = re.search('[0-9]+', line).group()
                self.chapters[chId] = Chapter()
                self.srtChapters.append(chId)

            elif line.startswith('[/ChID'):
                pass

            elif inScene:
                sceneText.append(line)

        return 'SUCCESS: ' + str(len(self.scenes)) + ' Scenes read from "' + self._filePath + '".'
