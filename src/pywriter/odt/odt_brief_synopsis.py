"""Provide a class for ODT brief synopsis export.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.odt.odt_file import OdtFile


class OdtBriefSynopsis(OdtFile):
    """ODT brief synopsis file representation.

    Export a brief synopsis with chapter titles and scene titles.
    """

    DESCRIPTION = 'Brief synopsis'
    SUFFIX = '_brf_synopsis'

    fileHeader = OdtFile.CONTENT_XML_HEADER + '''<text:p text:style-name="Title">$Title</text:p>
<text:p text:style-name="Subtitle">$AuthorName</text:p>
'''

    partTemplate = '''<text:h text:style-name="Heading_20_1" text:outline-level="1">$Title</text:h>
'''

    chapterTemplate = '''<text:h text:style-name="Heading_20_2" text:outline-level="2">$Title</text:h>
'''

    sceneTemplate = '''<text:p text:style-name="Text_20_body">$Title</text:p>
'''

    fileFooter = OdtFile.CONTENT_XML_FOOTER
