"""Provide a class for ODT item invisibly tagged descriptions export.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.odt.odt_file import OdtFile


class OdtItems(OdtFile):
    """ODT item descriptions file representation.

    Export a item sheet with invisibly tagged descriptions.
    """

    DESCRIPTION = 'Item descriptions'
    SUFFIX = '_items'

    fileHeader = OdtFile.CONTENT_XML_HEADER + '''<text:p text:style-name="Title">$Title</text:p>
<text:p text:style-name="Subtitle">$AuthorName</text:p>
'''

    itemTemplate = '''<text:h text:style-name="Heading_20_2" text:outline-level="2">$Title$AKA</text:h>
<text:section text:style-name="Sect1" text:name="ItID:$ID">
<text:p text:style-name="Text_20_body">$Desc</text:p>
</text:section>
'''

    fileFooter = OdtFile.CONTENT_XML_FOOTER

    def get_itemMapping(self, itId):
        """Return a mapping dictionary for an item section. 
        """
        itemMapping = OdtFile.get_itemMapping(self, itId)

        if self.items[itId].aka:
            itemMapping['AKA'] = ' ("' + self.items[itId].aka + '")'

        return itemMapping
