"""OdsItemList - Class for OpenDocument xml items table.

Part of the PyWriter project.
Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.ods.ods_builder import OdsBuilder
from pywriter.ods.ods_file import OdsFile


class OdsItemList(OdsFile):
    """OpenDocument xml items spreadsheet representation.
    """

    DESCRIPTION = 'Item list'
    SUFFIX = '_itemlist'

    fileHeader = OdsBuilder.CONTENT_XML_HEADER + '''<text:p text:style-name="Title">$Title</text:p>
<text:p text:style-name="Subtitle">$AuthorName</text:p>
'''

    itemTemplate = '''<text:h text:style-name="Heading_20_2" text:outline-level="2">$Title$AKA</text:h>
<text:section text:style-name="Sect1" text:name="ItID:$ID">
<text:p text:style-name="Text_20_body">$Desc</text:p>
</text:section>
'''

    fileFooter = OdsBuilder.CONTENT_XML_FOOTER

    def get_itemMapping(self, itId):
        """Return a mapping dictionary for an item section. 
        """
        itemMapping = OdsFile.get_itemMapping(self, itId)

        if self.items[itId].aka:
            itemMapping['AKA'] = ' ("' + self.items[itId].aka + '")'

        return itemMapping
