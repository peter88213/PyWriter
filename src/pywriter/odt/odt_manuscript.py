"""OdtManuscript - Class for OpenDocument xml file generation.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.odt.odt_template import OdtTemplate
from pywriter.odt.odt_file import OdtFile


class OdtManuscript(OdtFile):
    """OpenDocument xml manuscript file representation."""

    DESCRIPTION = 'Editable manuscript'
    SUFFIX = '_manuscript'

    fileHeader = OdtTemplate.CONTENT_XML_HEADER + '''<text:p text:style-name="Title">$Title</text:p>
<text:p text:style-name="Subtitle">$AuthorName</text:p>
'''

    partTemplate = '''<text:section text:style-name="Sect1" text:name="ChID:$ID">
<text:h text:style-name="Heading_20_1" text:outline-level="1"><text:a xlink:href="../${ProjectName}_parts.odt#ChID:$ID%7Cregion">$Title</text:a></text:h>
'''

    chapterTemplate = '''<text:section text:style-name="Sect1" text:name="ChID:$ID">
<text:h text:style-name="Heading_20_2" text:outline-level="2"><text:a xlink:href="../${ProjectName}_chapters.odt#ChID:$ID%7Cregion">$Title</text:a></text:h>
'''

    sceneTemplate = '''<text:section text:style-name="Sect1" text:name="ScID:$ID">
<text:p text:style-name="Text_20_body"><office:annotation>
<dc:creator>scene title</dc:creator>
<text:p>- $Title</text:p>
<text:p/>
<text:p><text:a xlink:href="../${ProjectName}_scenes.odt#ScID:$ID%7Cregion">→Summary</text:a> -</text:p>
</office:annotation>$SceneContent</text:p>
</text:section>
'''

    appendedSceneTemplate = '''<text:section text:style-name="Sect1" text:name="ScID:$ID">
<text:p text:style-name="First_20_line_20_indent"><office:annotation>
<dc:creator>scene title</dc:creator>
<text:p>- $Title</text:p>
<text:p/>
<text:p><text:a xlink:href="../${ProjectName}_scenes.odt#ScID:$ID%7Cregion">→Summary</text:a> -</text:p>
</office:annotation>$SceneContent</text:p>
</text:section>
'''

    sceneDivider = '''<text:p text:style-name="Heading_20_4">* * *</text:p>
'''

    chapterEndTemplate = '''</text:section>
'''

    fileFooter = OdtTemplate.CONTENT_XML_FOOTER

    def get_chapterSubst(self, chId, chapterNumber):
        chapterSubst = OdtFile.get_chapterSubst(self, chId, chapterNumber)

        if self.chapters[chId].suppressChapterTitle:
            chapterSubst['Title'] = ''

        return chapterSubst
