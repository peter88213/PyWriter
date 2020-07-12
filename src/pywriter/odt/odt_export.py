"""OdtFile - Class for OpenDocument xml file generation.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.odt.odt_template import OdtTemplate
from pywriter.odt.odt_file import OdtFile


class OdtExport(OdtFile):

    """OpenDocument xml project file representation."""

    fileHeader = OdtTemplate.CONTENT_XML_HEADER + '''<text:p text:style-name="Title">$Title</text:p>
<text:p text:style-name="Subtitle">$AuthorName</text:p>
'''

    partTemplate = '''<text:h text:style-name="Heading_20_1" text:outline-level="1">$Title</text:h>
'''

    chapterTemplate = '''<text:h text:style-name="Heading_20_2" text:outline-level="2">$Title</text:h>
'''

    sceneTemplate = '''<text:p text:style-name="Text_20_body"><office:annotation>
<dc:creator>scene title</dc:creator>
<text:p>$Title</text:p>
</office:annotation>$SceneContent</text:p>
'''

    sceneDivider = '''<text:p text:style-name="Heading_20_4">* * *</text:p>
'''

    fileFooter = OdtTemplate.CONTENT_XML_FOOTER
