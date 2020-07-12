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


class HtmlExport(Novel):
    _FILE_EXTENSION = 'html'
    # overwrites Novel._FILE_EXTENSION

    _HTML_HEADER = '/html_header.html'
    _HTML_FOOTER = '/html_footer.html'
    _CHAPTER_TEMPLATE = '/chapter_template.html'
    _SCENE_TEMPLATE = '/scene_template.html'
    _SCENE_DIVIDER = '/scene_divider.html'
    _CHARACTER_TEMPLATE = '/character_template.html'
    _LOCATION_TEMPLATE = '/location_template.html'
    _ITEM_TEMPLATE = '/item_template.html'

    def __init__(self, filePath, templatePath='.'):
        Novel.__init__(self, filePath)
        self.templatePath = templatePath

    def convert_markup(self, text):
        """Convert yw7 markup to target format."""

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

        # Initialize templates.

        result = read_html_file(self.templatePath + self._HTML_HEADER)

        if result[1] is not None:
            self.fileHeader = result[1]

        result = read_html_file(self.templatePath + self._CHAPTER_TEMPLATE)

        if result[1] is not None:
            self.chapterTemplate = result[1]

        result = read_html_file(self.templatePath + self._SCENE_TEMPLATE)

        if result[1] is not None:
            self.sceneTemplate = result[1]

        result = read_html_file(self.templatePath + self._SCENE_DIVIDER)

        if result[1] is not None:
            self.sceneDivider = result[1]

        result = read_html_file(self.templatePath + self._CHARACTER_TEMPLATE)

        if result[1] is not None:
            self.characterTemplate = result[1]

        result = read_html_file(self.templatePath + self._LOCATION_TEMPLATE)

        if result[1] is not None:
            self.locationTemplate = result[1]

        result = read_html_file(self.templatePath + self._ITEM_TEMPLATE)

        if result[1] is not None:
            self.itemTemplate = result[1]

        result = read_html_file(self.templatePath + self._HTML_FOOTER)

        if result[1] is not None:
            self.fileFooter = result[1]

        return Novel.write(self)
