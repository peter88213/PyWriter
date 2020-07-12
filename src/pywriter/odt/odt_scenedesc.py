"""OdtSceneDesc - Class for OpenDocument xml file generation.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from pywriter.odt.odt_template import OdtTemplate
from pywriter.odt.odt_file import OdtFile


class OdtSceneDesc(OdtFile):
    """OpenDocument xml scene summaries file representation."""

    fileHeader = OdtTemplate.CONTENT_XML_HEADER + '''<text:p text:style-name="Title">$Title</text:p>
<text:p text:style-name="Subtitle">$AuthorName</text:p>
'''

    partTemplate = '''<text:section text:style-name="Sect1" text:name="ChID:$ID">
<text:h text:style-name="Heading_20_1" text:outline-level="1"><text:a xlink:href="../yw7%20Sample%20Project_parts.odt#ChID:$ID%7Cregion">$Title</text:a></text:h>
'''

    chapterTemplate = '''<text:section text:style-name="Sect1" text:name="ChID:$ID">
<text:h text:style-name="Heading_20_2" text:outline-level="2"><text:a xlink:href="../yw7%20Sample%20Project_chapters.odt#ChID:$ID%7Cregion">$Title</text:a></text:h>
'''

    sceneTemplate = '''<text:section text:style-name="Sect1" text:name="ScID:$ID">
<text:p text:style-name="Text_20_body"><office:annotation>
<dc:creator>scene title</dc:creator>
<text:p>$Title</text:p>
<text:p/>
<text:p><text:a xlink:href="../yw7%20Sample%20Project_manuscript.odt#ScID:$ID%7Cregion">→Manuscript</text:a></text:p>
</office:annotation>$Desc</text:p>
</text:section>
'''

    sceneDivider = '''<text:p text:style-name="Heading_20_4">* * *</text:p>
'''

    chapterEndTemplate = '''</text:section>
'''

    characterTemplate = ''

    locationTemplate = ''

    itemTemplate = ''

    fileFooter = OdtTemplate.CONTENT_XML_FOOTER
