"""Provide a class for html visibly tagged chapters and scenes import.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import re
from pywriter.pywriter_globals import *
from pywriter.html.html_file import HtmlFile
from pywriter.model.splitter import Splitter


class HtmlProof(HtmlFile):
    """HTML proof reading file representation.

    Import a manuscript with visibly tagged chapters and scenes.
    """
    DESCRIPTION = _('Tagged manuscript for proofing')
    SUFFIX = '_proof'

    def __init__(self, filePath, **kwargs):
        """Initialize local instance variables for parsing.

        Positional arguments:
            filePath -- str: path to the file represented by the Novel instance.
            
        The HTML parser works like a state machine. 
        A prefix for chapter and scene recognition must be saved between the transitions.         
        Extends the superclass constructor.
        """
        super().__init__(filePath)
        self._prefix = None

    def _preprocess(self, text):
        """Process the html text before parsing.
        
        Convert html formatting tags to yWriter 7 raw markup.
        Overrides the superclass method.
        """
        return self._convert_to_yw(text)

    def _postprocess(self):
        """Parse the converted text to identify chapters and scenes.
        
        Overrides the superclass method.
        """
        sceneText = []
        scId = ''
        chId = ''
        inScene = False
        for line in self._lines:
            if '[ScID' in line:
                scId = re.search(r'[0-9]+', line).group()
                self.scenes[scId] = self.SCENE_CLASS()
                self.chapters[chId].srtScenes.append(scId)
                inScene = True
            elif '[/ScID' in line:
                self.scenes[scId].sceneContent = '\n'.join(sceneText)
                sceneText = []
                inScene = False
            elif '[ChID' in line:
                chId = re.search(r'[0-9]+', line).group()
                self.chapters[chId] = self.CHAPTER_CLASS()
                self.srtChapters.append(chId)
            elif '[/ChID' in line:
                pass
            elif inScene:
                sceneText.append(line)

    def handle_starttag(self, tag, attrs):
        """Recognize the paragraph's beginning.
        
        Positional arguments:
            tag -- str: name of the tag converted to lower case.
            attrs -- list of (name, value) pairs containing the attributes found inside the tag’s <> brackets.
        
        Overrides the superclass method.
        """
        if tag == 'p' and self._prefix is None:
            self._prefix = ''
        elif tag == 'h2':
            self._prefix = f'{Splitter.CHAPTER_SEPARATOR} '
        elif tag == 'h1':
            self._prefix = f'{Splitter.PART_SEPARATOR} '
        elif tag == 'li':
            self._prefix = f'{self._BULLET} '
        elif tag == 'blockquote':
            self._prefix = f'{self._INDENT} '

    def handle_endtag(self, tag):
        """Recognize the paragraph's end.      
        
        Positional arguments:
            tag -- str: name of the tag converted to lower case.

        Overrides HTMLparser.handle_endtag() called by the HTML parser to handle the end tag of an element.
        """
        if tag in ['p', 'h2', 'h1', 'blockquote']:
            self._prefix = None

    def handle_data(self, data):
        """Copy the scene paragraphs.      

        Positional arguments:
            data -- str: text to be stored. 
        
        Overrides HTMLparser.handle_data() called by the parser to process arbitrary data.
        """
        if self._prefix is not None:
            self._lines.append(f'{self._prefix}{data}')
