"""MdFile - Class for Markdown file operations and parsing.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
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
    """Markdown file representation of an yWriter project's OfficeFile part. 

    Represents a Markdown file with visible chapter and scene tags 
    to be converted by Pandoc.

    # Attributes

    _text : str
        contains the parsed data.

    _collectText : bool
        simple parsing state indicator. 
        True means: the data returned by the html parser 
        belongs to the body section. 

    # Methods

    read : str
        parse the Markdown file located at filePath, fetching 
        the Novel attributes.
        Return a message beginning with SUCCESS or ERROR. 

    write : str
        Arguments 
            novel : Novel
                the data to be written. 
        Generate a Markdown file containing:
        - chapter ID tags,
        - chapter headings,
        - scene ID tags, 
        - scene content.
        Return a message beginning with SUCCESS or ERROR.
    """

    _fileExtension = 'md'
    # overwrites PywFile._fileExtension

    def read(self):
        """Read data from markdown file with chapter and scene tags. """

        def to_yw7(text):
            """Convert markdown to yw7 raw markup. """

            text = text.replace('<sub>', '')
            text = text.replace('</sub>', '')
            # html tags misplaced by Pandoc.
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
        scId = ''
        chId = ''
        inScene = False

        lines = text.split('\n')

        for line in lines:

            if line.startswith('[ScID'):
                scId = re.search('[0-9]+', line).group()
                self.scenes[scId] = Scene()
                self.chapters[chId].srtScenes.append(scId)
                inScene = True

            elif line.startswith('[/ScID]'):
                self.scenes[scId].sceneContent = sceneText
                sceneText = ''
                inScene = False

            elif line.startswith('[ChID'):
                chId = re.search('[0-9]+', line).group()
                self.chapters[chId] = Chapter()
                self.srtChapters.append(chId)

            elif line.startswith('[/ChID]'):
                pass

            elif inScene:
                sceneText = sceneText + line + '\n'

        return('SUCCESS: ' + str(len(self.scenes)) + ' Scenes read from "' + self._filePath + '".')

    def write(self, novel) -> str:
        """Write novel attributes to Markdown file. """

        def format_chapter_title(text):
            """Fix auto-chapter titles for non-English. """

            text = text.replace('Chapter ', '')
            return(text)

        def to_md(text):
            """Convert yw7 specific markup. """

            text = text.replace('\n\n', '\n')
            text = text.replace('\n', '\n\n')
            text = text.replace('*', '\*')
            text = text.replace('[i]', '*')
            text = text.replace('[/i]', '*')
            text = text.replace('[b]', '**')
            text = text.replace('[/b]', '**')
            return(text)

        # Copy the novel's attributes to write

        if novel.srtChapters != []:
            self.srtChapters = novel.srtChapters

        if novel.scenes is not None:
            self.scenes = novel.scenes

        if novel.chapters is not None:
            self.chapters = novel.chapters

        text = ''

        for chId in self.srtChapters:
            text = text + '\\[ChID:' + chId + '\\]\n'
            headingMarker = MD_HEADING_MARKERS[self.chapters[chId].type]
            text = text + headingMarker + \
                format_chapter_title(self.chapters[chId].title) + '\n'

            for scId in self.chapters[chId].srtScenes:
                text = text + '\\[ScID:' + scId + '\\]\n'

                try:
                    text = text + self.scenes[scId].sceneContent + '\n'

                except(TypeError):
                    text = text + '\n'

                text = text + '\\[/ScID\\]\n'

            text = text + '\\[/ChID\\]\n'

        text = to_md(text)

        try:
            with open(self._filePath, 'w', encoding='utf-8') as f:
                f.write(text)

        except(PermissionError):
            return('ERROR: ' + self._filePath + '" is write protected.')

        return('SUCCESS: "' + self._filePath + '" saved.')
