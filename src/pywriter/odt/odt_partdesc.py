"""OdtPartDesc - Class for OpenDocument xml file generation.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from pywriter.odt.odt_template import OdtTemplate
from pywriter.odt.odt_file import OdtFile


class OdtPartDesc(OdtFile):
    """OpenDocument xml part summaries file representation."""

    fileHeader = OdtTemplate.CONTENT_XML_HEADER + '''<text:p text:style-name="Title">$Title</text:p>
<text:p text:style-name="Subtitle">$AuthorName</text:p>
'''

    partTemplate = '''<text:h text:style-name="Heading_20_1" text:outline-level="1"><text:a xlink:href="../yw7%20Sample%20Project_manuscript.odt#ChID:$ID%7Cregion">$Title</text:a></text:h>
<text:section text:style-name="Sect1" text:name="ChID:$ID">
<text:p text:style-name="Text_20_body">$Desc</text:p>
</text:section>
'''

    chapterTemplate = ''

    sceneTemplate = ''

    sceneDivider = ''

    chapterEndTemplate = ''

    characterTemplate = ''

    locationTemplate = ''

    itemTemplate = ''

    fileFooter = OdtTemplate.CONTENT_XML_FOOTER
