"""OdtCharacters - Class for OpenDocument xml file generation.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.odt.odt_builder import OdtBuilder
from pywriter.odt.odt_file import OdtFile


class OdtCharacters(OdtFile):
    """OpenDocument xml character descriptions file representation.
    """

    DESCRIPTION = 'Character descriptions'
    SUFFIX = '_characters'

    fileHeader = OdtBuilder.CONTENT_XML_HEADER + '''<text:p text:style-name="Title">$Title</text:p>
<text:p text:style-name="Subtitle">$AuthorName</text:p>
'''

    characterTemplate = '''<text:h text:style-name="Heading_20_2" text:outline-level="2">$Title$FullName$AKA</text:h>
<text:section text:style-name="Sect1" text:name="CrID:$ID">
<text:h text:style-name="Heading_20_3" text:outline-level="3">Description</text:h>
<text:section text:style-name="Sect1" text:name="CrID_desc:$ID">
<text:p text:style-name="Text_20_body">$Desc</text:p>
</text:section>
<text:h text:style-name="Heading_20_3" text:outline-level="3">Bio</text:h>
<text:section text:style-name="Sect1" text:name="CrID_bio:$ID">
<text:p text:style-name="Text_20_body">$Bio</text:p>
</text:section>
<text:h text:style-name="Heading_20_3" text:outline-level="3">Goals</text:h>
<text:section text:style-name="Sect1" text:name="CrID_goals:$ID">
<text:p text:style-name="Text_20_body">$Goals</text:p>
</text:section>
</text:section>
'''

    fileFooter = OdtBuilder.CONTENT_XML_FOOTER

    def get_characterMapping(self, crId):
        """Return a mapping dictionary for a character section. 
        """
        characterMapping = OdtFile.get_characterMapping(self, crId)

        if self.characters[crId].aka:
            characterMapping['AKA'] = ' ("' + self.characters[crId].aka + '")'

        if self.characters[crId].fullName:
            characterMapping['FullName'] = '/' + self.characters[crId].fullName

        return characterMapping
