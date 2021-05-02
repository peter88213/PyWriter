#!/usr/bin/env python3
"""Class for Markdown file processing. 

Part of the PyWriter project.
Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import re

from pywriter.file.file_export import FileExport
from pywriter.model.chapter import Chapter
from pywriter.model.scene import Scene


class MdFile(FileExport):
    """Markdown file representation
    """

    DESCRIPTION = 'Markdown converter'
    EXTENSION = '.md'
    SUFFIX = ''

    SCENE_DIVIDER = '* * *'

    fileHeader = '''**${Title}**  
  
*${AuthorName}*  
  
'''

    partTemplate = '\n# ${Title}\n\n'

    chapterTemplate = '\n## ${Title}\n\n'

    sceneTemplate = '${SceneContent}\n\n'

    sceneDivider = '\n\n' + SCENE_DIVIDER + '\n\n'

    def __init__(self, filePath, markdownMode=False):
        FileExport.__init__(self, filePath)
        self.markdownMode = markdownMode

    def get_chapterMapping(self, chId, chapterNumber):
        """Return a mapping dictionary for a chapter section. 
        """
        chapterMapping = FileExport.get_chapterMapping(
            self, chId, chapterNumber)

        if self.chapters[chId].suppressChapterTitle:
            chapterMapping['Title'] = ''

        return chapterMapping

    def convert_from_yw(self, text):
        """Convert yw7 markup to Markdown.
        """

        MD_REPLACEMENTS = [
            ['\n', '\n\n'],
            ['[i]', '*'],
            ['[/i]', '*'],
            ['[b]', '**'],
            ['[/b]', '**'],
            ['/*', '<!---'],
            ['*/', '--->'],
            ['  ', ' '],
        ]

        try:

            for r in MD_REPLACEMENTS:
                text = text.replace(r[0], r[1])

            # Remove highlighting, alignment,
            # strikethrough, and underline tags.

            text = re.sub('\[\/*[h|c|r|s|u]\d*\]', '', text)

        except AttributeError:
            text = ''

        return(text)

    def convert_to_yw(self, text):
        """Convert Markdown to yw7 markup.
        """
        if not self.markdownMode:
            SAFE_SCENE_DIVIDER = '~ ~ ~'

            # Save the scene dividers: they may contain asterisks
            # TODO: Better find a regex-based solution

            text = text.replace(self.SCENE_DIVIDER, SAFE_SCENE_DIVIDER)

            def set_bold(i):
                return '[b]' + i.group(1) + '[/b]'

            def set_italic(i):
                return '[i]' + i.group(1) + '[/i]'

            boldMd = re.compile('\*\*(.+?)\*\*')
            text = boldMd.sub(set_bold, text)

            italicMd = re.compile('\*(.+?)\*')
            text = italicMd.sub(set_italic, text)

            # Restore the scene dividers

            text = text.replace(SAFE_SCENE_DIVIDER, self.SCENE_DIVIDER)

            MD_REPLACEMENTS = [
                ['\n\n', '\n'],
                ['<!---', '/*'],
                ['--->', '*/'],
            ]

            try:

                for r in MD_REPLACEMENTS:
                    text = text.replace(r[0], r[1])

            except AttributeError:
                text = ''

        return(text)

    def read(self):
        """Parse the Markdown file located at filePath
        Return a message beginning with SUCCESS or ERROR.
        """
        LOW_WORDCOUNT = 10

        def write_scene_content(scId, lines):

            if scId is not None:
                self.scenes[scId].sceneContent = '\n'.join(lines)

                if self.scenes[scId].wordCount < LOW_WORDCOUNT:
                    self.scenes[scId].status = Scene.STATUS.index('Outline')

                else:
                    self.scenes[scId].status = Scene.STATUS.index('Draft')

        chCount = 0
        scCount = 0
        lines = []
        chId = None
        scId = None

        try:
            with open(self.filePath, encoding='utf-8') as f:
                mdText = f.read()
                cnvText = self.convert_to_yw(mdText)
                mdLines = (cnvText).split('\n')

        except(FileNotFoundError):
            return 'ERROR: "' + os.path.normpath(self.filePath) + '" not found.'

        except:
            return 'ERROR: Can not parse "' + os.path.normpath(self.filePath) + '".'

        for mdLine in mdLines:

            if mdLine.startswith('#'):

                # Write previous scene.

                write_scene_content(scId, lines)
                scId = None

                # Add a chapter.

                chCount += 1
                chId = str(chCount)
                self.chapters[chId] = Chapter()

                title = mdLine.split('# ')[1]

                self.chapters[chId].title = title
                self.srtChapters.append(chId)
                self.chapters[chId].oldType = '0'

                if mdLine.startswith('# '):
                    self.chapters[chId].chLevel = 1

                else:
                    self.chapters[chId].chLevel = 0

                self.chapters[chId].srtScenes = []

            elif self.SCENE_DIVIDER in mdLine:

                # Write previous scene.

                write_scene_content(scId, lines)
                scId = None

            elif scId is not None:
                lines.append(mdLine)

            elif chId is not None:

                # Add a scene.

                scCount += 1
                scId = str(scCount)

                self.scenes[scId] = Scene()
                self.chapters[chId].srtScenes.append(scId)
                self.scenes[scId].status = '1'
                self.scenes[scId].title = 'Scene ' + str(scCount)

                lines = [mdLine]

        return 'SUCCESS'
