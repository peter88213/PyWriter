""" PyWriter module

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import re
from pywriter.core.pywfile import PywFile
from pywriter.core.chapter import Chapter
from pywriter.core.scene import Scene

MD_HEADING_MARKERS = ("##", "#")
# Index is yWriter's chapter type:
# 0 is for an ordinary chapter
# 1 is for a chapter beginning a section


class MdFile(PywFile):
    """yWriter project linked to a markdown file. """

    _fileExtension = 'md'

    def read(self):
        """Read data from markdown project file. """

        def format_yw7(text):
            """Convert markdown to yw7 raw markup. """

            text = text.replace('\r', '\n')
            text = text.replace('\n\n', '\n')
            text = text.replace('\[', '[')
            text = text.replace('\]', ']')
            text = text.replace('\\*', '_asterisk_')
            text = re.sub('\*\*(.+?)\*\*', '[b]\g<1>[/b]', text)
            text = re.sub('\*(.+?)\*', '[i]\g<1>[/i]', text)
            text = text.replace('_asterisk_', '*')
            return(text)

        try:
            with open(self._filePath, 'r', encoding='utf-8') as f:
                text = (f.read())
        except(FileNotFoundError):
            return('ERROR: "' + self._filePath + '" not found.')

        text = format_yw7(text)

        sceneText = ''
        scID = ''
        chID = ''
        inScene = False

        lines = text.split('\n')
        for line in lines:
            if line.count('[ScID'):
                scID = re.search('[0-9]+', line).group()
                self.scenes[scID] = Scene()
                self.chapters[chID].scenes.append(scID)
                inScene = True
            elif line.count('[/ScID]'):
                self.scenes[scID].sceneContent = sceneText
                sceneText = ''
                inScene = False
            elif line.count('[ChID'):
                chID = re.search('[0-9]+', line).group()
                self.chapters[chID] = Chapter()
            elif line.count('[/ChID]'):
                pass
            elif inScene:
                sceneText = sceneText + line + '\n'
        return('SUCCESS: ' + str(len(self.scenes)) + ' Scenes read from "' + self._filePath + '".')

    def get_text(self):
        """Format project text to markdown. """

        def format_chapter_title(text):
            """Fix auto-chapter titles for non-English """

            text = text.replace('Chapter ', '')
            return(text)

        def format_md(text):
            """Convert yw7 specific markup """

            text = text.replace('\n\n', '\n')
            text = text.replace('\n', '\n\n')
            text = text.replace('*', '\*')
            text = text.replace('[i]', '*')
            text = text.replace('[/i]', '*')
            text = text.replace('[b]', '**')
            text = text.replace('[/b]', '**')
            return(text)

        text = ''
        for chID in self.chapters:
            text = text + '\\[ChID:' + chID + '\\]\n'
            headingMarker = MD_HEADING_MARKERS[self.chapters[chID].type]
            text = text + headingMarker + \
                format_chapter_title(self.chapters[chID].title) + '\n'
            for scID in self.chapters[chID].scenes:
                text = text + '\\[ScID:' + scID + '\\]\n'
                try:
                    text = text + self.scenes[scID].sceneContent + '\n'
                except(TypeError):
                    text = text + '\n'
                text = text + '\\[/ScID\\]\n'
            text = text + '\\[/ChID\\]\n'
        text = format_md(text)
        return(text)
