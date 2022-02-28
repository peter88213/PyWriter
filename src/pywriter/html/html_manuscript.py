"""Provide a class for html invisibly tagged chapters and scenes import.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.html.html_file import HtmlFile
from pywriter.model.splitter import Splitter


class HtmlManuscript(HtmlFile):
    """HTML manuscript file representation.

    Import a manuscript with invisibly tagged chapters and scenes.
    """
    DESCRIPTION = 'Editable manuscript'
    SUFFIX = '_manuscript'

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
            if tag == 'h1':
                self._lines.append(Splitter.PART_SEPARATOR)
            elif tag == 'h2':
                self._lines.append(Splitter.CHAPTER_SEPARATOR)

    def handle_comment(self, data):
        """Process inline comments within scene content.
        
        Positional arguments:
            data -- str: comment text. 
        
        Use marked comments at scene start as scene titles.
        Overrides the superclass method.
        """
        if self._scId is not None: 
            if not self._lines:
                # Comment is at scene start
                if self._SC_TITLE_BRACKET in data:
                    # Comment is marked as a scene title
                    try:   
                        self.scenes[self._scId].title = data.split(self._SC_TITLE_BRACKET)[1].strip()
                    except:
                        pass
                    return

            self._lines.append(f'{self._COMMENT_START}{data.strip()}{self._COMMENT_END}')
            

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
        elif self._chId is not None:
            if tag == 'div':
                self._chId = None

    def handle_data(self, data):
        """Collect data within scene sections.

        Positional arguments:
            data -- str: text to be stored. 
        
        Overrides HTMLparser.handle_data() called by the parser when a comment is encountered.
        """
        if self._scId is not None:
            if not data.isspace():
                self._lines.append(data)
        elif self._chId is not None:
            if not self.chapters[self._chId].title:
                self.chapters[self._chId].title = data.strip()
