"""HtmlOutline - Class for html outline file parsing.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from html import unescape

from pywriter.html.html_manuscript import HtmlManuscript
from pywriter.html.html_form import *


class HtmlOutline(HtmlManuscript):
    """HTML file representation of an yWriter project's OfficeFile part.

    Represents a html file without chapter and scene tags 
    to be written by Open/LibreOffice Writer.
    """

    def read(self):
        """Parse a HTML file and insert chapter and scene sections.
        Insert chapter and scene descriptions.
        Return a message beginning with SUCCESS or ERROR. 
        """
        _TEXT_END_TAGS = ['<div type=footer>', '/body']

        result = read_html_file(self._filePath)

        if result[0].startswith('ERROR'):
            return (result[0])

        # Insert chapter and scene markers in html text.

        lines = result[1].split('\n')
        newlines = []
        chCount = 0     # overall chapter count
        scCount = 0     # overall scene count

        contentFinished = False
        inSceneSection = False
        inChapterSection = False

        chapterTitles = {}
        sceneTitles = {}
        chapterDescs = {}
        sceneDescs = {}
        chapterLevels = {}

        headingLine = ''

        tagRegEx = re.compile(r'(<!--.*?-->|<[^>]*>)')
        scDesc = ''
        chDesc = ''

        for line in lines:

            if contentFinished:
                break

            line = line.rstrip().lstrip()
            scan = line.lower()

            if '</h1' in scan or '</h2' in scan:
                line = headingLine + line
                scan = line.lower()
                headingLine = ''
                inChapterSection = True

                if inSceneSection:

                    # Close the previous scene section.

                    newlines.append('</DIV>')

                    # Write back scene description.

                    sceneDescs[str(scCount)] = scDesc
                    scDesc = ''
                    inSceneSection = False

                if chCount > 0:

                    # Close the previous chapter section.

                    newlines.append('</DIV>')

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

                m = re.search('<[h,H][1,2].*?>(.+?)</[h,H][1,2]>', line)

                if m is not None:
                    chapterTitles[str(chCount)] = m.group(1)

                else:
                    chapterTitles[str(chCount)] = 'Chapter ' + str(chCount)

                # Open the next chapter section.

                newlines.append('<DIV ID="ChID:' + str(chCount) + '">')

            elif '<h1' in scan or '<h2' in scan:
                headingLine = line

            elif '</h3' in scan:
                line = headingLine + line
                scan = line.lower()
                headingLine = ''

                # a new scene begins

                if inSceneSection:

                    # Close the previous scene section.

                    newlines.append('</DIV>')

                    # Write back previous scene description.

                    sceneDescs[str(scCount)] = scDesc
                    scDesc = ''

                scCount += 1

                # Get scene title.

                m = re.search('<[h,H]3.*?>(.+?)</[h,H]3>', line)

                if m is not None:
                    sceneTitles[str(scCount)] = m.group(1)

                else:
                    sceneTitles[str(scCount)] = 'Scene ' + str(scCount)

                # Open the next scene section.

                newlines.append('<DIV ID="ScID:' + str(scCount) + '">')
                inSceneSection = True

            elif '<h3' in scan:
                headingLine = line

            elif inChapterSection:

                for marker in _TEXT_END_TAGS:

                    if marker in scan:

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
                            inChapterSection = False

                        contentFinished = True
                        break

                if inSceneSection:

                    if scDesc != '' and '<p' in scan:
                        scDesc += '\n'

                    elif scDesc != '':
                        scDesc += ' '

                    scDesc += unescape(tagRegEx.sub('', line))

                elif inChapterSection:

                    if chDesc != '' and '<p' in scan:
                        chDesc += '\n'

                    elif chDesc != '':
                        chDesc += ' '

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

            self.scenes[scId].status = 1

        for chId in self.chapters:
            self.chapters[chId].title = chapterTitles[chId]
            self.chapters[chId].chLevel = chapterLevels[chId]
            self.chapters[chId].chType = 0
            self.chapters[chId].suppressChapterTitle = False

            if chId in chapterDescs:
                self.chapters[chId].desc = chapterDescs[chId]

        return 'SUCCESS: ' + str(len(self.scenes)) + ' Scenes read from "' + self._filePath + '".'
