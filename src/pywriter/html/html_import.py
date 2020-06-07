"""HtmlImport - Class for html import file parsing.

Part of the PyWriter project.
Copyright (c) 2020, peter88213
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

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

        result = read_html_file(self._filePath)

        if result[0].startswith('ERROR'):
            return (result[0])

        # Insert chapter and scene markers in html text.

        lines = result[1].split('\n')
        newlines = []
        chCount = 0     # overall chapter count
        scCount = 0     # overall scene count
        LocScCount = 0  # chapter local scene count
        finished = False

        chapterTitles = {}
        chapterLevels = {}

        for line in lines:

            line = line.rstrip().lstrip()
            scan = line.lower()

            if ('<h1' in scan) or ('<h2' in scan):
                chCount += 1

                if '<h1' in scan:
                    # line contains the start of a part heading
                    chapterLevels[str(chCount)] = 1

                else:
                    # line contains the start of a chapter heading
                    chapterLevels[str(chCount)] = 0

                if LocScCount > 0:
                    newlines.append('</DIV>')
                    # close the leading scene section
                    LocScCount = 0

                if chCount > 0:
                    newlines.append('</DIV>')
                    # close the leading chapter section

                m = re.match('.+?>(.+?)</[h,H][1,2]>', line)

                if m is not None:
                    chapterTitles[str(chCount)] = m.group(1)

                else:
                    chapterTitles[str(chCount)] = 'Chapter' + str(chCount)

                newlines.append('<DIV ID="ChID:' + str(chCount) + '">')
                # open the next chapter section

            elif _SCENE_DIVIDER in scan:

                if LocScCount > 0:
                    newlines.append('</DIV>')
                    # close the leading scene section

                LocScCount += 1
                scCount += 1
                line = '<DIV ID="ScID:' + str(scCount) + '">'
                # open the next scene section

            elif (chCount > 0) and (LocScCount == 0) and ('<p' in scan):
                LocScCount += 1
                scCount += 1
                newlines.append('<DIV ID="ScID:' + str(scCount) + '">')
                # open the chapter's first scene section

            elif not finished and '<p' in scan:
                pass

            else:
                for marker in _TEXT_END_TAGS:

                    if not finished and (marker in scan):
                        # line contains the start of a chapter heading

                        if LocScCount > 0:
                            newlines.append('</DIV>')
                            # close the last scene section

                        if chCount > 0:
                            newlines.append('</DIV>')
                            # close the last chapter section

                        finished = True
                        break

            newlines.append(line)

        text = '\n'.join(newlines)
        text = to_yw7(text)

        # Invoke HTML parser.

        self.feed(text)

        for scId in self.scenes:
            self.scenes[scId].title = 'Scene ' + scId

            if self.scenes[scId].wordCount < _LOW_WORDCOUNT:
                self.scenes[scId].status = 1

            else:
                self.scenes[scId].status = 2

        for chId in self.chapters:
            self.chapters[chId].title = chapterTitles[chId]
            self.chapters[chId].chLevel = chapterLevels[chId]
            self.chapters[chId].type = 0
            self.chapters[chId].suppressChapterTitle = True

        return 'SUCCESS: ' + str(len(self.scenes)) + ' Scenes read from "' + self._filePath + '".'
