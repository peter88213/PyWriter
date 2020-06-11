"""HtmlImport - Class for html import file parsing.

Part of the PyWriter project.
Copyright (c) 2020, peter88213
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import re
from html import unescape

from pywriter.html.html_manuscript import HtmlManuscript
from pywriter.html.html_form import *


class HtmlImport(HtmlManuscript):
    """HTML file representation of an yWriter project's OfficeFile part.

    Represents a html file without chapter and scene tags 
    to be written by Open/LibreOffice Writer.
    """

    def read(self):
        """Parse a HTML file and insert chapter and scene sections.
        Read scene contents.
        Return a message beginning with SUCCESS or ERROR. 
        """
        _TEXT_END_TAGS = ['<div type=footer>', '/body']
        _SCENE_DIVIDER = '* * *'
        _LOW_WORDCOUNT = 10

        # Enum substitute for the state machine

        _ST_INITIAL = 0
        _ST_AFTER_CHAPTER_HEADING = 1
        _ST_CHAPTER_DESC = 2
        _ST_AFTER_SCENE_HEADING = 3
        _ST_SCENE_DESC = 4
        _ST_SCENE_CONTENT = 5
        _ST_FINISHED = 6

        result = read_html_file(self._filePath)

        if result[0].startswith('ERROR'):
            return (result[0])

        # Insert chapter and scene markers in html text.

        lines = result[1].split('\n')
        newlines = []
        chCount = 0     # overall chapter count
        scCount = 0     # overall scene count

        chapterTitles = {}
        sceneTitles = {}
        chapterDescs = {}
        sceneDescs = {}
        chapterLevels = {}

        HtmlTagRegex = re.compile(r'(<!--.*?-->|<[^>]*>)')
        chapterHeadingRegex = re.compile('.+?>(.+?)</[h,H][1,2]>')
        sceneHeadingRegex = re.compile('.+?>(.+?)</[h,H]3>')

        desc = ''
        state = _ST_INITIAL

        for line in lines:

            line = line.rstrip().lstrip()
            scan = line.lower()

            if state == _ST_INITIAL:

                if '<h1' in scan or '<h2' in scan:
                    chCount += 1

                    if '<h1' in scan:
                        # line contains the start of a part heading
                        chapterLevels[str(chCount)] = 1

                    else:
                        # line contains the start of a chapter heading
                        chapterLevels[str(chCount)] = 0

                    m = chapterHeadingRegex.match(line)
    
                    if m is not None:
                        chapterTitles[str(chCount)] = m.group(1)
    
                    else:
                        chapterTitles[str(chCount)] = 'Chapter' + str(chCount)

                    newlines.append('<DIV ID="ChID:' + str(chCount) + '">')
                    # open the next chapter section
                state = _ST_AFTER_CHAPTER_HEADING

            elif state == _ST_AFTER_CHAPTER_HEADING:

            elif state == _SEARCH:
                if '<h3' in scan:
                    scCount += 1
                    m = sceneHeadingRegex.match(line)

                    if m is not None:
                        sceneTitles[str(scCount)] = m.group(1)

                    else:
                        sceneTitles[str(scCount)] = 'Scene ' + str(scCount)

                    newlines.append('<DIV ID="ScID:' + str(scCount) + '">')
                    # open a scene section
                    state = _ST_AFTER_SCENE_HEADING

                elif '<p' in scan:

                    if '{#' in scan:
                        desc += unescape(HtmlTagRegex.sub('', line).replace(
                            '{#', '').replace('#}', ''))

                        if '#}' in scan:
                            chapterDescs[str(chCount)] = desc
                            desc = ''

                        else:
                            state = _ST_CHAPTER_DESC

                    else:
                        newlines.append('<DIV ID="ScID:' + str(scCount) + '">')
                        # open a scene section

                        if '{{' in scan:
                            desc += unescape(HtmlTagRegex.sub('', line).replace(
                                '{{', '').replace('}}', ''))

                            if '}}' in scan:
                                sceneDescs[str(scCount)] = desc
                                desc = ''
                                state = _ST_SCENE_CONTENT

                            else:
                                state = _ST_SCENE_DESC

                        else:
                            newlines.append(line)
                            state = _ST_SCENE_CONTENT

            elif state == _ST_CHAPTER_DESC:
                desc += '\n' + unescape(HtmlTagRegex.sub('', line).replace(
                    '{#', '').replace('#}', ''))

                if '#}' in scan:
                    chapterDescs[str(chCount)] = desc
                    desc = ''
                    state = _ST_AFTER_CHAPTER_HEADING

            elif state == _ST_SCENE_DESC:
                desc += '\n' + unescape(HtmlTagRegex.sub('', line).replace(
                    '{{', '').replace('}}', ''))

                if '}}' in scan:
                    sceneDescs[str(scCount)] = desc
                    desc = ''
                    state = _ST_SCENE_CONTENT

            elif state == _ST_AFTER_SCENE_HEADING:

                if '<p' in scan:

                    if '{{' in scan:
                        desc += unescape(HtmlTagRegex.sub('', line).replace(
                            '{{', '').replace('}}', ''))

                        if '}}' in scan:
                            sceneDescs[str(scCount)] = desc
                            desc = ''
                            state = _ST_SCENE_CONTENT

                        else:
                            state = _ST_SCENE_DESC
                            
                    else:
                        newlines.append(line)
                        state = _ST_SCENE_CONTENT

            elif state == _ST_SCENE_CONTENT:



        text = '\n'.join(newlines)
        text = to_yw7(text)

        # Invoke HTML parser.

        self.feed(text)

        for scId in self.scenes:
            self.scenes[scId].title = sceneTitles[scId]

            if scId in sceneDescs:
                self.scenes[scId].desc = sceneDescs[scId]

            if self.scenes[scId].wordCount < _LOW_WORDCOUNT:
                self.scenes[scId].status = 1

            else:
                self.scenes[scId].status = 2

        for chId in self.chapters:
            self.chapters[chId].title = chapterTitles[chId]
            self.chapters[chId].chLevel = chapterLevels[chId]
            self.chapters[chId].type = 0
            self.chapters[chId].suppressChapterTitle = True

            if chId in chapterDescs:
                self.chapters[chId].desc = chapterDescs[chId]

        return 'SUCCESS: ' + str(len(self.scenes)) + ' Scenes read from "' + self._filePath + '".'
