""" PyWriter module

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import re
from pywriter.model.pywfile import PywFile
from pywriter.model.chapter import Chapter
from pywriter.model.scene import Scene

MD_HEADING_MARKERS = ("##", "#")
# Index is yWriter's chapter type:
# 0 is for an ordinary chapter
# 1 is for a chapter beginning a section


class MdFile(PywFile):
    """yWriter project linked to a markdown file. """

    _fileExtension = 'md'

    def read(self):
        """Read data from markdown project file. """

        def to_yw7(text):
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

        text = to_yw7(text)

        sceneText = ''
        scID = ''
        chID = ''
        inScene = False

        lines = text.split('\n')
        for line in lines:
            if line.startswith('[ScID'):
                scID = re.search('[0-9]+', line).group()
                self.scenes[scID] = Scene()
                self.chapters[chID].scenes.append(scID)
                inScene = True
            elif line.startswith('[/ScID]'):
                self.scenes[scID].sceneContent = sceneText
                sceneText = ''
                inScene = False
            elif line.startswith('[ChID'):
                chID = re.search('[0-9]+', line).group()
                self.chapters[chID] = Chapter()
            elif line.startswith('[/ChID]'):
                pass
            elif inScene:
                sceneText = sceneText + line + '\n'
        return('SUCCESS: ' + str(len(self.scenes)) + ' Scenes read from "' + self._filePath + '".')

    def write(self, novel) -> str:
        """Format project text to markdown. """

        def format_chapter_title(text):
            """Fix auto-chapter titles for non-English """

            text = text.replace('Chapter ', '')
            return(text)

        def to_md(text):
            """Convert yw7 specific markup """

            text = text.replace('\n\n', '\n')
            text = text.replace('\n', '\n\n')
            text = text.replace('*', '\*')
            text = text.replace('[i]', '*')
            text = text.replace('[/i]', '*')
            text = text.replace('[b]', '**')
            text = text.replace('[/b]', '**')
            return(text)

        if novel.title is not None:
            if novel.title != '':
                self.title = novel.title

        if novel.scenes is not None:
            self.scenes = novel.scenes

        if novel.chapters is not None:
            self.chapters = novel.chapters

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
        text = to_md(text)

        try:
            with open(self._filePath, 'w', encoding='utf-8') as f:
                f.write(text)
                # get_text() is to be overwritten
                # by file format specific subclasses.
        except(PermissionError):
            return('ERROR: ' + self._filePath + '" is write protected.')

        return('SUCCESS: "' + self._filePath + '" saved.')
