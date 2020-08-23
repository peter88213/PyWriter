"""OdtProof - Class for OpenDocument xml file generation.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.odt.odt_template import OdtTemplate
from pywriter.odt.odt_file import OdtFile


class OdtProof(OdtFile):
    """OpenDocument xml proof reading file representation."""

    SUFFIX = '_proof'

    fileHeader = OdtTemplate.CONTENT_XML_HEADER + '''<text:p text:style-name="Title">$Title</text:p>
<text:p text:style-name="Subtitle">$AuthorName</text:p>
'''

    partTemplate = '''<text:p text:style-name="yWriter_20_mark">[ChID:$ID]</text:p>
<text:h text:style-name="Heading_20_1" text:outline-level="1">$Title</text:h>
'''

    chapterTemplate = '''<text:p text:style-name="yWriter_20_mark">[ChID:$ID]</text:p>
<text:h text:style-name="Heading_20_2" text:outline-level="2">$Title</text:h>
'''

    unusedChapterTemplate = '''<text:p text:style-name="yWriter_20_mark_20_unused">[ChID:$ID (Unused)]</text:p>
<text:h text:style-name="Heading_20_2" text:outline-level="2">$Title</text:h>
'''

    noteChapterTemplate = '''<text:p text:style-name="yWriter_20_mark_20_info">[ChID:$ID (Info)]</text:p>
<text:h text:style-name="Heading_20_2" text:outline-level="2">$Title</text:h>
'''

    sceneTemplate = '''<text:p text:style-name="yWriter_20_mark">[ScID:$ID]</text:p>
<text:p text:style-name="Text_20_body">$SceneContent</text:p>
<text:p text:style-name="yWriter_20_mark">[/ScID]</text:p>
'''

    unusedSceneTemplate = '''<text:p text:style-name="yWriter_20_mark_20_unused">[ScID:$ID (Unused)]</text:p>
<text:p text:style-name="Text_20_body">$SceneContent</text:p>
<text:p text:style-name="yWriter_20_mark_20_unused">[/ScID (Unused)]</text:p>
'''

    noteSceneTemplate = '''<text:p text:style-name="yWriter_20_mark_20_info">[ScID:$ID (Info)]</text:p>
<text:p text:style-name="Text_20_body">$SceneContent</text:p>
<text:p text:style-name="yWriter_20_mark_20_info">[/ScID (Info)]</text:p>
'''

    sceneDivider = '''<text:p text:style-name="Heading_20_4">* * *</text:p>
'''

    chapterEndTemplate = '''<text:p text:style-name="yWriter_20_mark">[/ChID]</text:p>
'''

    unusedChapterEndTemplate = '''<text:p text:style-name="yWriter_20_mark_20_unused">[/ChID (Unused)]</text:p>
'''

    infoChapterEndTemplate = '''<text:p text:style-name="yWriter_20_mark_20_info">[/ChID (Info)]</text:p>
'''

    fileFooter = OdtTemplate.CONTENT_XML_FOOTER
