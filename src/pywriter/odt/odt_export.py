"""Provide a class for ODT chapters and scenes export.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.odt.odt_file import OdtFile


class OdtExport(OdtFile):
    """ODT novel file representation.

    Export a non-reimportable manuscript with chapters and scenes.
    """
    fileHeader = OdtFile.CONTENT_XML_HEADER + '''<text:p text:style-name="Title">$Title</text:p>
<text:p text:style-name="Subtitle">$AuthorName</text:p>
'''

    partTemplate = '''<text:h text:style-name="Heading_20_1" text:outline-level="1">$Title</text:h>
'''

    chapterTemplate = '''<text:h text:style-name="Heading_20_2" text:outline-level="2">$Title</text:h>
'''

    sceneTemplate = '''<text:p text:style-name="Text_20_body"><office:annotation>
<dc:creator>scene title</dc:creator>
<text:p>~ ${Title} ~</text:p>
</office:annotation>$SceneContent</text:p>
'''

    appendedSceneTemplate = '''<text:p text:style-name="First_20_line_20_indent"><office:annotation>
<dc:creator>scene title</dc:creator>
<text:p>~ ${Title} ~</text:p>
</office:annotation>$SceneContent</text:p>
'''

    sceneDivider = '<text:p text:style-name="Heading_20_4">* * *</text:p>\n'
    #sceneDivider = '<text:p text:style-name="Heading_20_5"></text:p>\n'

    fileFooter = OdtFile.CONTENT_XML_FOOTER

    def get_chapterMapping(self, chId, chapterNumber):
        """Return a mapping dictionary for a chapter section. 
        """
        chapterMapping = OdtFile.get_chapterMapping(self, chId, chapterNumber)

        if self.chapters[chId].suppressChapterTitle:
            chapterMapping['Title'] = ''

        return chapterMapping
