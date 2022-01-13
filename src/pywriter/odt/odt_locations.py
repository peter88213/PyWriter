"""Provide a class for ODT invisibly tagged location descriptions export.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.odt.odt_file import OdtFile


class OdtLocations(OdtFile):
    """ODT location descriptions file representation.

    Export a location sheet with invisibly tagged descriptions.
    """

    DESCRIPTION = 'Location descriptions'
    SUFFIX = '_locations'

    fileHeader = OdtFile.CONTENT_XML_HEADER + '''<text:p text:style-name="Title">$Title</text:p>
<text:p text:style-name="Subtitle">$AuthorName</text:p>
'''

    locationTemplate = '''<text:h text:style-name="Heading_20_2" text:outline-level="2">$Title$AKA</text:h>
<text:section text:style-name="Sect1" text:name="LcID:$ID">
<text:p text:style-name="Text_20_body">$Desc</text:p>
</text:section>
'''

    fileFooter = OdtFile.CONTENT_XML_FOOTER

    def get_locationMapping(self, lcId):
        """Return a mapping dictionary for a location section. 
        """
        locationMapping = super().get_locationMapping(lcId)

        if self.locations[lcId].aka:
            locationMapping['AKA'] = ' ("' + self.locations[lcId].aka + '")'

        return locationMapping
