"""HtmlExport - Class for html export with templates.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from html import escape
from string import Template

from pywriter.model.novel import Novel
from pywriter.model.scene import Scene
from pywriter.html.html_form import read_html_file

# Template files

HTML_HEADER = 'html_header.html'
HTML_FOOTER = 'html_footer.html'
CHAPTER_TEMPLATE = 'chapter_template.html'
SCENE_TEMPLATE = 'scene_template.html'
SCENE_DIVIDER = 'scene_divider.html'


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
                text = escape(text)
                text = text.replace('\n', '</p>\n<p>')
                text = text.replace('[i]', '<em>')
                text = text.replace('[/i]', '</em>')
                text = text.replace('[b]', '<strong>')
                text = text.replace('[/b]', '</strong>')
                text = text.replace('<p></p>', '<p><br /></p>')

            else:
                text = ''

            return(text)

        # Initialize templates.

        result = read_html_file(HTML_HEADER)

        if result[1] is not None:
            htmlHeader = result[1]

        else:
            htmlHeader = '''<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<title>$Title</title>
</head>
<body>
'''

        result = read_html_file(CHAPTER_TEMPLATE)

        if result[1] is not None:
            chapterTemplate = result[1]

        else:
            chapterTemplate = '''<h2>$Title</h2>
'''

        result = read_html_file(SCENE_TEMPLATE)

        if result[1] is not None:
            sceneTemplate = result[1]

        else:
            sceneTemplate = '''
<p>$SceneContent</p>
'''

        result = read_html_file(SCENE_DIVIDER)

        if result[1] is not None:
            sceneDivider = result[1]

        else:
            sceneDivider = '''
<h4>* * *</h4>
'''

        result = read_html_file(HTML_FOOTER)

        if result[1] is not None:
            htmlFooter = result[1]

        else:
            htmlFooter = '''</body>
</html>
'''

        lines = []

        # Append html header template and fill in.

        htmlHeaderSubst = dict(
            Title=self.title,
            Desc=to_html(self.desc),
            AuthorName=self.author,
            FieldTitle1=self.fieldTitle1,
            FieldTitle2=self.fieldTitle2,
            FieldTitle3=self.fieldTitle3,
            FieldTitle4=self.fieldTitle4,
        )

        htmlTemplate = Template(htmlHeader)
        lines.append(htmlTemplate.safe_substitute(htmlHeaderSubst))

        for chId in self.srtChapters:

            if self.chapters[chId].isUnused:
                continue

            if self.chapters[chId].chType != 0:
                continue

            # Append chapter template and fill in.

            chapterSubst = dict(
                Title=self.chapters[chId].title,
                Desc=to_html(self.chapters[chId].desc),
            )

            htmlTemplate = Template(chapterTemplate)
            lines.append(htmlTemplate.safe_substitute(chapterSubst))

            firstSceneInChapter = True

            for scId in self.chapters[chId].srtScenes:

                if self.scenes[scId].isUnused:
                    continue

                if self.scenes[scId].doNotExport:
                    continue

                if not (firstSceneInChapter or self.scenes[scId].appendToPrev):
                    lines.append(sceneDivider)

                # Prepare data for substitution.

                if self.scenes[scId].tags is not None:
                    sceneTags = ','.join(self.scenes[scId].tags)

                else:
                    sceneTags = ''

                if self.scenes[scId].characters is not None:
                    sChList = []

                    for chId in self.scenes[scId].characters:
                        sChList.append(self.characters[chId].title)

                    sceneChars = ','.join(sChList)

                    viewpointChar = sChList[0]

                else:
                    sceneChars = ''
                    viewpointChar = ''

                if self.scenes[scId].locations is not None:
                    sLcList = []

                    for lcId in self.scenes[scId].locations:
                        sLcList.append(self.locations[lcId].title)

                    sceneLocs = ','.join(sLcList)

                else:
                    sceneLocs = ''

                if self.scenes[scId].items is not None:
                    sItList = []

                    for itId in self.scenes[scId].items:
                        sItList.append(self.items[itId].title)

                    sceneItems = ','.join(sItList)

                else:
                    sceneItems = ''

                if self.scenes[scId].isReactionScene:
                    reactionScene = 'R'

                else:
                    reactionScene = 'A'

                # Append scene template and fill in.

                sceneSubst = dict(
                    Title=self.scenes[scId].title,
                    Desc=to_html(self.scenes[scId].desc),
                    WordCount=str(self.scenes[scId].wordCount),
                    LetterCount=str(self.scenes[scId].letterCount),
                    Status=Scene.STATUS[self.scenes[scId].status],
                    SceneContent=to_html(self.scenes[scId].sceneContent),
                    FieldTitle1=self.fieldTitle1,
                    FieldTitle2=self.fieldTitle2,
                    FieldTitle3=self.fieldTitle3,
                    FieldTitle4=self.fieldTitle4,
                    Field1=self.scenes[scId].field1,
                    Field2=self.scenes[scId].field2,
                    Field3=self.scenes[scId].field3,
                    Field4=self.scenes[scId].field4,
                    ReactionScene=reactionScene,
                    Goal=to_html(self.scenes[scId].goal),
                    Conflict=to_html(self.scenes[scId].conflict),
                    Outcome=to_html(self.scenes[scId].outcome),
                    Tags=sceneTags,
                    Characters=sceneChars,
                    Viewpoint=viewpointChar,
                    Locations=sceneLocs,
                    Items=sceneItems,
                    Notes=to_html(self.scenes[scId].sceneNotes),
                )

                htmlTemplate = Template(sceneTemplate)
                lines.append(htmlTemplate.safe_substitute(sceneSubst))

                firstSceneInChapter = False

        # Append html footer and fill in.

        lines.append(htmlFooter)
        text = '\n'.join(lines)

        try:
            with open(self.filePath, 'w', encoding='utf-8') as f:
                f.write(text)

        except:
            return 'ERROR: Cannot write "' + self.filePath + '".'

        return 'SUCCESS: Content written to "' + self.filePath + '".'
