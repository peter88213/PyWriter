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

        _SC_DESC_OPEN = '{_'
        _SC_DESC_CLOSE = '_}'
        _CH_DESC_OPEN = '{#'
        _CH_DESC_CLOSE = '#}'
        _OUTLINE_OPEN = '{outline}'
        _OUTLINE_CLOSE = '{/outline}'

        result = read_html_file(self._filePath)

        if result[0].startswith('ERROR'):
            return (result[0])

        # Insert chapter and scene markers in html text.

        lines = result[1].split('\n')
        newlines = []
        chCount = 0     # overall chapter count
        scCount = 0     # overall scene count

        lastChDone = 0
        lastScDone = 0

        outlineMode = False
        inBody = False
        contentFinished = False
        inSceneSection = False
        inSceneDescription = False
        inChapterDescription = False

        chapterTitles = {}
        sceneTitles = {}
        chapterDescs = {}
        sceneDescs = {}
        chapterLevels = {}

        tagRegEx = re.compile(r'(<!--.*?-->|<[^>]*>)')
        scDesc = ''
        chDesc = ''

        for line in lines:

            if contentFinished:
                break

            line = line.rstrip().lstrip()
            scan = line.lower()

            if _OUTLINE_OPEN in scan:
                outlineMode = True

            elif _OUTLINE_CLOSE in scan:
                outlineMode = False

            elif '<h1' in scan or '<h2' in scan:
                inBody = True

                if inSceneDescription or inChapterDescription:
                    return 'ERROR: Wrong description tags in Chapter #' + str(chCount)

                if inSceneSection:

                    # Close the previous scene section.

                    newlines.append('</DIV>')

                    if outlineMode:

                        # Write back scene description.

                        sceneDescs[str(scCount)] = scDesc
                        scDesc = ''

                    inSceneSection = False

                if chCount > 0:

                    # Close the previous chapter section.

                    newlines.append('</DIV>')

                    if outlineMode:

                        # Write back previous chapter description.

                        chapterDescs[str(chCount)] = chDesc
                        chDesc = ''

                chCount += 1

                if '<h1' in scan:
                    # line contains the start of a part heading
                    chapterLevels[str(chCount)] = 1

                else:
                    # line contains the start of a chapter heading
                    chapterLevels[str(chCount)] = 0

                # Get part/chapter title.

                m = re.match('.+?>(.+?)</[h,H][1,2]>', line)

                if m is not None:
                    chapterTitles[str(chCount)] = m.group(1)

                else:
                    chapterTitles[str(chCount)] = 'Chapter' + str(chCount)

                # Open the next chapter section.

                newlines.append('<DIV ID="ChID:' + str(chCount) + '">')

            elif _SCENE_DIVIDER in scan or '<h3' in scan:
                # a new scene begins

                if inSceneDescription or inChapterDescription:
                    return 'ERROR: Wrong description tags in Chapter #' + str(chCount)

                if inSceneSection:

                    # Close the previous scene section.

                    newlines.append('</DIV>')

                    if outlineMode:

                        # write back previous scene description.

                        sceneDescs[str(scCount)] = scDesc
                        scDesc = ''

                scCount += 1

                # Get scene title.

                m = re.match('.+?>(.+?)</[h,H]3>', line)

                if m is not None:
                    sceneTitles[str(scCount)] = m.group(1)

                else:
                    sceneTitles[str(scCount)] = 'Scene ' + str(scCount)

                # Open the next scene section.

                newlines.append('<DIV ID="ScID:' + str(scCount) + '">')
                inSceneSection = True

            elif inBody and '<p' in scan:

                # Process a new paragraph.

                if inChapterDescription or _CH_DESC_OPEN in scan:

                    # Add a tagged chapter description.

                    if chDesc != '':
                        chDesc += '\n'

                    chDesc += unescape(tagRegEx.sub('', line).replace(
                        _CH_DESC_OPEN, '').replace(_CH_DESC_CLOSE, ''))

                    if _CH_DESC_CLOSE in scan:
                        chapterDescs[str(chCount)] = chDesc
                        chDesc = ''
                        inChapterDescription = False

                    else:
                        inChapterDescription = True

                elif chCount > 0 and not inSceneSection:
                    scCount += 1

                    # Generate scene title.

                    sceneTitles[str(scCount)] = 'Scene ' + str(scCount)

                    # Open a scene section without heading.

                    newlines.append('<DIV ID="ScID:' + str(scCount) + '">')
                    inSceneSection = True

                    if _SC_DESC_OPEN in scan:

                        scDesc += unescape(tagRegEx.sub('', line).replace(
                            _SC_DESC_OPEN, '').replace(_SC_DESC_CLOSE, ''))

                        if _SC_DESC_CLOSE in scan:
                            sceneDescs[str(scCount)] = scDesc
                            scDesc = ''

                        else:
                            inSceneDescription = True

                    elif outlineMode:

                        # Begin a new paragraph in the chapter description.

                        if chDesc != '':
                            chDesc += '\n'

                        chDesc += unescape(tagRegEx.sub('', line))

                    else:
                        newlines.append(line)

                elif inSceneDescription or _SC_DESC_OPEN in scan:

                    # Add a tagged scene description.

                    if scDesc != '':
                        scDesc += '\n'

                    scDesc += unescape(tagRegEx.sub('', line).replace(
                        _SC_DESC_OPEN, '').replace(_SC_DESC_CLOSE, ''))

                    if _SC_DESC_CLOSE in scan:
                        sceneDescs[str(scCount)] = scDesc
                        scDesc = ''
                        inSceneDescription = False

                    else:
                        inSceneDescription = True

                elif outlineMode:

                    if str(scCount) in sceneTitles:

                        # Begin a new paragraph in the scene description.

                        if scDesc != '':
                            scDesc += '\n'

                        scDesc += unescape(tagRegEx.sub('', line))

                    else:

                        # Begin a new paragraph in the chapter description.

                        if chDesc != '':
                            chDesc += '\n'

                        chDesc += unescape(tagRegEx.sub('', line))

                else:
                    newlines.append(line)

            elif inChapterDescription:
                chDesc += '\n' + unescape(tagRegEx.sub('', line).replace(
                    _CH_DESC_OPEN, '').replace(_CH_DESC_CLOSE, ''))

                if _CH_DESC_CLOSE in scan:
                    chapterDescs[str(chCount)] = chDesc
                    chDesc = ''
                    inChapterDescription = False

            elif inSceneDescription:
                scDesc += '\n' + unescape(tagRegEx.sub('', line).replace(
                    _SC_DESC_OPEN, '').replace(_SC_DESC_CLOSE, ''))

                if _SC_DESC_CLOSE in scan:
                    sceneDescs[str(scCount)] = scDesc
                    scDesc = ''
                    inSceneDescription = False

            else:
                for marker in _TEXT_END_TAGS:

                    if marker in scan:

                        # Finish content processing.

                        if outlineMode:

                            # Write back last descriptions.

                            chapterDescs[str(chCount)] = chDesc
                            sceneDescs[str(scCount)] = scDesc

                        if inSceneSection:

                            # Close the last scene section.

                            newlines.append('</DIV>')
                            inSceneSection = False

                        if chCount > 0:

                            # Close the last chapter section.

                            newlines.append('</DIV>')

                        contentFinished = True
                        break

                if not contentFinished:

                    if outlineMode:

                        if str(scCount) in sceneTitles:

                            # Add line to the scene description.

                            scDesc += unescape(tagRegEx.sub('', line))

                        else:

                            # Add line to the chapter description.

                            chDesc += unescape(tagRegEx.sub('', line))

                    else:
                        newlines.append(line)

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
