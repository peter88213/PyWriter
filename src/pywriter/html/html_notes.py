"""Provide a class for html invisibly tagged "Notes" chapters import.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.html.html_manuscript import HtmlManuscript
from pywriter.model.splitter import Splitter


class HtmlNotes(HtmlManuscript):
    """HTML "Notes" chapters file representation.

    Import a manuscript with invisibly tagged chapters and scenes.
    """
    DESCRIPTION = 'Notes chapters'
    SUFFIX = '_notes'

    def _postprocess(self):
        """Make all chapters and scenes "Notes" type.
        
        Overrides the superclass method.
        """
        for chId in self.srtChapters:
            self.chapters[chId].chType = 1
            for scId in self.chapters[chId].srtScenes:
                self.scenes[scId].isNotesScene = True

