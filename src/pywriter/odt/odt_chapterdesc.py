"""OdtChapterDesc - Class for OpenDocument xml file generation.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.odt.odt_builder import OdtBuilder
from pywriter.odt.odt_file import OdtFile


class OdtChapterDesc(OdtFile):
    """OpenDocument xml chapter summaries file representation.
    """

    DESCRIPTION = 'Chapter descriptions'
    SUFFIX = '_chapters'

    fileHeader = OdtBuilder.CONTENT_XML_HEADER + '''<text:p text:style-name="Title">$Title</text:p>
<text:p text:style-name="Subtitle">$AuthorName</text:p>
'''

    partTemplate = '''<text:h text:style-name="Heading_20_1" text:outline-level="1"><text:a xlink:href="../${ProjectName}_parts.odt#ChID:$ID%7Cregion">$Title</text:a></text:h>
'''

    chapterTemplate = '''<text:h text:style-name="Heading_20_2" text:outline-level="2"><text:a xlink:href="../${ProjectName}_manuscript.odt#ChID:$ID%7Cregion">$Title</text:a></text:h>
<text:section text:style-name="Sect1" text:name="ChID:$ID">
<text:p text:style-name="Text_20_body">$Desc</text:p>
</text:section>
'''

    fileFooter = OdtBuilder.CONTENT_XML_FOOTER
