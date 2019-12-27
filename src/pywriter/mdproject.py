""" PyWriter module

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import re
from pywriter.pywproject import PywProject


HEADING_MARKER = ("##", "#")


class MdProject(PywProject):
    """ yWriter project linked to an yw7 project file. """

    def __init__(self, fileName):
        PywProject.__init__(self)
        self.fileName = fileName

    def read(self):
        """ Read data from markdown project file. """

        def format_yw7(text):
            """ Convert markdown to yw7 raw markup. """
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
            with open(self.fileName, 'r', encoding='utf-8') as f:
                text = (f.read())
        except(FileNotFoundError):
            return('\nERROR: "' + self.fileName + '" not found.')

        text = format_yw7(text)

        sceneText = ''
        scID = ''
        chID = ''
        inScene = False

        lines = text.split('\n')
        for line in lines:
            if line.count('[ScID'):
                scID = re.search('[0-9]+', line).group()
                self.scenes[scID] = PywProject.Scene()
                self.chapters[chID].scenes.append(scID)
                inScene = True
            elif line.count('[/ScID]'):
                self.scenes[scID].sceneContent = sceneText
                sceneText = ''
                inScene = False
            elif line.count('[ChID'):
                chID = re.search('[0-9]+', line).group()
                self.chapters[chID] = PywProject.Chapter()
            elif line.count('[/ChID]'):
                pass
            elif inScene:
                sceneText = sceneText + line + '\n'

    def getText(self):
        """ Format project text to markdown. """

        def format_chapter_title(text):
            """ Fix auto-chapter titles for non-English """
            text = text.replace('Chapter ', '')
            return(text)

        def format_md(text):
            """ Convert yw7 specific markup """
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
            headingMarker = HEADING_MARKER[self.chapters[chID].type]
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

    def write(self):
        """ Write attributes to markdown project file. """

        with open(self.fileName, 'w', encoding='utf-8') as f:
            f.write(self.getText())

        return('\nSUCCESS: ' + str(len(self.scenes)) + ' Scenes written to "' + self.fileName + '".')
