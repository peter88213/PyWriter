"""HtmlImport - Class for html import file parsing.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
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

        headingLine = ''

        for line in lines:

            if contentFinished:
                break

            line = line.rstrip().lstrip()
            scan = line.lower()

            if '</h1' in scan or '</h2' in scan or '</h3' in scan:
                line = headingLine + line
                scan = line.lower()
                headingLine = ''
                inBody = True

                if inSceneDescription or inChapterDescription:
                    return 'ERROR: Wrong description tags in Chapter #' + str(chCount)

                if inSceneSection:

                    # Close the previous scene section.

                    newlines.append('</DIV>')
                    inSceneSection = False

                if chCount > 0:

                    # Close the previous chapter section.

                    newlines.append('</DIV>')

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

            elif _SCENE_DIVIDER in scan or '<h3' in scan:
                # a new scene begins

                if inSceneDescription or inChapterDescription:
                    return 'ERROR: Wrong description tags in Chapter #' + str(chCount)

                if inSceneSection:

                    # Close the previous scene section.

                    newlines.append('</DIV>')

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

            elif inBody and '<p' in scan:

                # Process a new paragraph.

                if chCount > 0 and not inSceneSection:
                    scCount += 1

                    # Generate scene title.

                    sceneTitles[str(scCount)] = 'Scene ' + str(scCount)

                    # Open a scene section without heading.

                    newlines.append('<DIV ID="ScID:' + str(scCount) + '">')
                    inSceneSection = True
                    newlines.append(line)

                else:
                    newlines.append(line)

            else:
                for marker in _TEXT_END_TAGS:

                    if marker in scan:

                        # Finish content processing.

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
            self.chapters[chId].chType = 0
            self.chapters[chId].suppressChapterTitle = False

            if chId in chapterDescs:
                self.chapters[chId].desc = chapterDescs[chId]

        return 'SUCCESS: ' + str(len(self.scenes)) + ' Scenes read from "' + self._filePath + '".'
