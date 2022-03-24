"""Provide a class for html invisibly tagged "Notes" chapters import.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.html.html_file import HtmlFile
from pywriter.model.splitter import Splitter


class HtmlNotes(HtmlFile):
    """HTML "Notes" chapters file representation.

    Import a manuscript with invisibly tagged chapters and scenes.
    """
    DESCRIPTION = 'Notes chapters'
    SUFFIX = '_notes'

    def _preprocess(self, text):
        """Process the html text before parsing.
        
        Convert html formatting tags to yWriter 7 raw markup.
        Overrides the superclass method.
        """
        return self._convert_to_yw(text)

    def handle_starttag(self, tag, attrs):
        """Identify scenes and chapters.
        
        Positional arguments:
            tag -- str: name of the tag converted to lower case.
            attrs -- list of (name, value) pairs containing the attributes found inside the tag’s <> brackets.
        
        Extends the superclass method by processing inline chapter and scene dividers.
        """
        super().handle_starttag(tag, attrs)
        if self._scId is not None:
            self._getScTitle = False
            if tag == 'h3':
                if self.scenes[self._scId].title is None:
                    self._getScTitle = True
                else:
                    self._lines.append(Splitter.SCENE_SEPARATOR)
            elif tag == 'h2':
                self._lines.append(Splitter.CHAPTER_SEPARATOR)
            elif tag == 'h1':
                self._lines.append(Splitter.PART_SEPARATOR)

    def handle_endtag(self, tag):
        """Recognize the end of the scene section and save data.
        
        Positional arguments:
            tag -- str: name of the tag converted to lower case.

        Overrides HTMLparser.handle_endtag() called by the HTML parser to handle the end tag of an element.
        """
        if self._scId is not None:
            if tag == 'div':
                text = ''.join(self._lines)
                self.scenes[self._scId].sceneContent = text
                self._lines = []
                self._scId = None
            elif tag == 'p':
                self._lines.append('\n')
            elif tag == 'h1':
                self._lines.append('\n')
            elif tag == 'h2':
                self._lines.append('\n')
            elif tag == 'h3' and not self._getScTitle:
                self._lines.append('\n')
        elif self._chId is not None:
            if tag == 'div':
                self._chId = None

    def handle_data(self, data):
        """Collect data within scene sections.

        Positional arguments:
            data -- str: text to be stored. 
        
        Overrides HTMLparser.handle_data() called by the parser to process arbitrary data.
        """
        if self._scId is not None:
            if self._getScTitle:
                self.scenes[self._scId].title = data.strip()
            elif not data.isspace():
                self._lines.append(data)
        elif self._chId is not None:
            if self.chapters[self._chId].title is None:
                self.chapters[self._chId].title = data.strip()

    def _postprocess(self):
        """Make all chapters and scenes "Notes" type.
        
        Overrides the superclass method.
        """
        for chId in self.srtChapters:
            self.chapters[chId].chType = 1
            for scId in self.chapters[chId].srtScenes:
                self.scenes[scId].isNotesScene = True

