"""OdtFile - Class for OpenDocument xml file generation.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.odt.odt_builder import OdtBuilder
from pywriter.odt.odt_file import OdtFile


class OdtExport(OdtFile):

    SUFFIX = ''

    """OpenDocument xml project file representation."""

    fileHeader = OdtBuilder.CONTENT_XML_HEADER + '''<text:p text:style-name="Title">$Title</text:p>
<text:p text:style-name="Subtitle">$AuthorName</text:p>
'''

    partTemplate = '''<text:h text:style-name="Heading_20_1" text:outline-level="1">$Title</text:h>
'''

    chapterTemplate = '''<text:h text:style-name="Heading_20_2" text:outline-level="2">$Title</text:h>
'''

    sceneTemplate = '''<text:p text:style-name="Text_20_body"><office:annotation>
<dc:creator>scene title</dc:creator>
<text:p>- $Title</text:p>
</office:annotation>$SceneContent</text:p>
'''

    appendedSceneTemplate = '''<text:p text:style-name="First_20_line_20_indent"><office:annotation>
<dc:creator>scene title</dc:creator>
<text:p>- $Title</text:p>
</office:annotation>$SceneContent</text:p>
'''

    sceneDivider = '''<text:p text:style-name="Heading_20_4">* * *</text:p>
'''

    fileFooter = OdtBuilder.CONTENT_XML_FOOTER

    def get_chapterSubst(self, chId, chapterNumber):
        chapterSubst = OdtFile.get_chapterSubst(self, chId, chapterNumber)

        if self.chapters[chId].suppressChapterTitle:
            chapterSubst['Title'] = ''

        return chapterSubst
