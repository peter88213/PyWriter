"""OdtLocations - Class for OpenDocument xml file generation.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.odt.odt_template import OdtTemplate
from pywriter.odt.odt_file import OdtFile


class OdtLocations(OdtFile):
    """OpenDocument xml location descriptions file representation."""

    DESCRIPTION = 'Location descriptions'
    SUFFIX = '_locations'

    def get_locationSubst(self, lcId):
        locationSubst = OdtFile.get_locationSubst(self, lcId)

        if self.locations[lcId].aka:
            locationSubst['AKA'] = ' ("' + self.locations[lcId].aka + '")'

        return locationSubst

    fileHeader = OdtTemplate.CONTENT_XML_HEADER + '''<text:p text:style-name="Title">$Title</text:p>
<text:p text:style-name="Subtitle">$AuthorName</text:p>
'''

    locationTemplate = '''<text:h text:style-name="Heading_20_2" text:outline-level="2">$Title$AKA</text:h>
<text:section text:style-name="Sect1" text:name="ItID:$ID">
<text:p text:style-name="Text_20_body">$Desc</text:p>
</text:section>
'''

    fileFooter = OdtTemplate.CONTENT_XML_FOOTER
