"""OdsLocList - Class for OpenDocument xml locations table.

Part of the PyWriter project.
Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.ods.ods_builder import OdsBuilder
from pywriter.ods.ods_file import OdsFile


class OdsLocList(OdsFile):
    """OpenDocument xml locations spreadsheet representation.
    """

    DESCRIPTION = 'Location list'
    SUFFIX = '_loclist'

    fileHeader = OdsBuilder.CONTENT_XML_HEADER + '''<text:p text:style-name="Title">$Title</text:p>
<text:p text:style-name="Subtitle">$AuthorName</text:p>
'''

    locationTemplate = '''<text:h text:style-name="Heading_20_2" text:outline-level="2">$Title$AKA</text:h>
<text:section text:style-name="Sect1" text:name="LcID:$ID">
<text:p text:style-name="Text_20_body">$Desc</text:p>
</text:section>
'''

    fileFooter = OdsBuilder.CONTENT_XML_FOOTER

    def get_locationMapping(self, lcId):
        """Return a mapping dictionary for a location section. 
        """
        locationMapping = OdsFile.get_locationMapping(self, lcId)

        if self.locations[lcId].aka:
            locationMapping['AKA'] = ' ("' + self.locations[lcId].aka + '")'

        return locationMapping
