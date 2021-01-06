"""OdtItems - Class for OpenDocument xml file generation.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.odt.odt_builder import OdtBuilder
from pywriter.odt.odt_file import OdtFile


class OdtItems(OdtFile):
    """OpenDocument xml item descriptions file representation.
    """

    DESCRIPTION = 'Item descriptions'
    SUFFIX = '_items'

    fileHeader = OdtBuilder.CONTENT_XML_HEADER + '''<text:p text:style-name="Title">$Title</text:p>
<text:p text:style-name="Subtitle">$AuthorName</text:p>
'''

    itemTemplate = '''<text:h text:style-name="Heading_20_2" text:outline-level="2">$Title$AKA</text:h>
<text:section text:style-name="Sect1" text:name="ItID:$ID">
<text:p text:style-name="Text_20_body">$Desc</text:p>
</text:section>
'''

    fileFooter = OdtBuilder.CONTENT_XML_FOOTER

    def get_itemMapping(self, itId):
        """Return a mapping dictionary for an item section. 
        """
        itemMapping = OdtFile.get_itemMapping(self, itId)

        if self.items[itId].aka:
            itemMapping['AKA'] = ' ("' + self.items[itId].aka + '")'

        return itemMapping
