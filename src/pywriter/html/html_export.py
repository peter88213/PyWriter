"""HtmlExport - Class for html export with templates.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from string import Template
from pywriter.model.novel import Novel


class HtmlExport(Novel):

    _FILE_EXTENSION = 'html'
    # overwrites Novel._FILE_EXTENSION

    def merge(self, novel):
        """Copy selected novel attributes.
        """

        if novel.title is None:
            self.title = ''

        else:
            self.title = novel.title

        if novel.desc is None:
            self.desc = ''

        else:
            self.desc = novel.desc

        if novel.author is None:
            self.author = ''

        else:
            self.author = novel.author

        if novel.srtChapters != []:
            self.srtChapters = novel.srtChapters

        if novel.scenes is not None:
            self.scenes = novel.scenes

        if novel.chapters is not None:
            self.chapters = novel.chapters

        if novel.characters is not None:
            self.characters = novel.characters

        if novel.locations is not None:
            self.locations = novel.locations

        if novel.items is not None:
            self.items = novel.items

    def write(self):

        def to_html(text):
            """Convert yw7 markup to html."""

            if text is not None:
                text = text.replace('\n', '</p>\n<p>')
                text = text.replace('[i]', '<em>')
                text = text.replace('[/i]', '</em>')
                text = text.replace('[b]', '<strong>')
                text = text.replace('[/b]', '</strong>')
                text = text.replace('<p></p>', '<p><br /></p>')

            else:
                text = ''

            return(text)

        # Templates

        htmlHeader = '''<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<style type="text/css">
h1, h2, h3, h4, p {font: 1em monospace; margin: 3em; line-height: 1.5em}
h1, h2, h3, h4 {text-align: center}
h1 {letter-spacing: 0.5em; font-style: italic}
h1, h2 {font-weight: bold}
h3 {font-style: italic}
p {margin-top:0; margin-bottom:0}
p+p {margin-top:0; margin-bottom:0; text-indent: 1em}
strong {font-weight:normal; text-transform: uppercase}
</style>
<title>$bookTitle</title>
</head>
<body>
<div align="center">
<p><strong>$bookTitle</strong></p>
<p>by</p>
<p><strong>$authorName</strong></p>
</div>
'''

        chapterHeading = '''<h2>$chapterTitle</h2>
'''

        sceneComplete = '''
<p>$sceneContent</p>
'''

        sceneDivider = '''
<h4>* * *</h4>
'''

        htmlFooter = '''</body>
</html>
'''

        lines = []

        # Append html header template and fill in.

        s = Template(htmlHeader)
        g = dict(bookTitle=self.title, authorName=self.author)
        lines.append(s.safe_substitute(g))

        for chId in self.srtChapters:

            if self.chapters[chId].isUnused:
                continue

            if self.chapters[chId].chType != 0:
                continue

            # Append chapter heading template and fill in.

            s = Template(chapterHeading)
            c = dict(chapterTitle=self.chapters[chId].title)
            lines.append(s.safe_substitute(c))

            firstSceneInChapter = True

            for scId in self.chapters[chId].srtScenes:

                if self.scenes[scId].isUnused:
                    continue

                if self.scenes[scId].doNotExport:
                    continue

                if not (firstSceneInChapter or self.scenes[scId].appendToPrev):
                    lines.append(sceneDivider)

                # Append scene template and fill in.

                s = Template(sceneComplete)
                d = dict(sceneTitle=self.scenes[scId].title, sceneContent=to_html(
                    self.scenes[scId].sceneContent))
                lines.append(s.safe_substitute(d))

                firstSceneInChapter = False

        # Append html footer and fill in.

        text = '\n'.join(lines)

        try:
            with open(self.filePath, 'w', encoding='utf-8') as f:
                f.write(text)

        except:
            return 'ERROR: Cannot write "' + self.filePath + '".'

        return 'SUCCESS: Content written to "' + self.filePath + '".'
