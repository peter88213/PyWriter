"""Provide a class for ODT invisibly tagged "Todo" chapters export.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from string import Template
from pywriter.pywriter_globals import *
from pywriter.odt_w.odt_w_manuscript import OdtWManuscript


class OdtWTodo(OdtWManuscript):
    """ODT "Todo" chapters file writer.

    Export a manuscript with invisibly tagged chapters and scenes.
    """
    DESCRIPTION = _('Todo chapters')
    SUFFIX = '_todo'

    _partTemplate = ''
    _chapterTemplate = ''
    _chapterEndTemplate = ''
    _sceneTemplate = ''
    _appendedSceneTemplate = ''

    _todoPartTemplate = '''<text:section text:style-name="Sect1" text:name="ChID:$ID">
<text:h text:style-name="Heading_20_1" text:outline-level="1">$Title</text:h>
'''

    _todoChapterTemplate = '''<text:section text:style-name="Sect1" text:name="ChID:$ID">
<text:h text:style-name="Heading_20_2" text:outline-level="2">$Title</text:h>
'''

    _todoSceneTemplate = '''<text:h text:style-name="Heading_20_3" text:outline-level="3">$Title</text:h>
<text:section text:style-name="Sect1" text:name="ScID:$ID">
<text:p text:style-name="Text_20_body">$SceneContent</text:p>
</text:section>
'''
    _sceneDivider = ''

    _todoChapterEndTemplate = '''</text:section>
'''

