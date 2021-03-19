"""OdtXref - Class for OpenDocument xml file generation.

Create cross reference lists.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.odt.odt_file import OdtFile


class OdtXref(OdtFile):
    """OpenDocument xml cross reference file representation.
    """

    DESCRIPTION = 'Cross reference'
    SUFFIX = '_xref'

    fileHeader = OdtFile.CONTENT_XML_HEADER + '''<text:p text:style-name="Title">$Title</text:p>
<text:p text:style-name="Subtitle">$AuthorName</text:p>
'''

    characterTemplate = '''<text:h text:style-name="Heading_20_2" text:outline-level="2">Scenes with Character $Title:</text:h><text:p text:style-name="Hanging_20_indent">$Scenes</text:p>
'''
    locationTemplate = '''<text:h text:style-name="Heading_20_2" text:outline-level="2">Scenes with Location $Title:</text:h><text:p text:style-name="Hanging_20_indent">$Scenes</text:p>
'''
    itemTemplate = '''<text:h text:style-name="Heading_20_2" text:outline-level="2">Scenes with Item $Title:</text:h><text:p text:style-name="Hanging_20_indent">$Scenes</text:p>
'''
    chrTagsTemplate = '''<text:h text:style-name="Heading_20_2" text:outline-level="2">Characters tagged $Tag:</text:h><text:p text:style-name="Hanging_20_indent">$Elements</text:p>
'''
    locTagsTemplate = '''<text:h text:style-name="Heading_20_2" text:outline-level="2">Locations tagged $Tag:</text:h><text:p text:style-name="Hanging_20_indent">$Elements</text:p>
'''
    itmTagsTemplate = '''<text:h text:style-name="Heading_20_2" text:outline-level="2">Items tagged $Tag:</text:h><text:p text:style-name="Hanging_20_indent">$Elements</text:p>
'''
    scnTagsTemplate = '''<text:h text:style-name="Heading_20_2" text:outline-level="2">Scenes tagged $Tag:</text:h><text:p text:style-name="Hanging_20_indent">$Elements</text:p>
'''
    fileFooter = OdtFile.CONTENT_XML_FOOTER

    def get_characterMapping(self, crId):
        """Return a mapping dictionary for a character section. 
        """
        characterMapping = OdtFile.get_characterMapping(self, crId)
        characterMapping['Scenes'] = characterMapping['Scenes'].replace(
            '\n', '</text:p><text:p text:style-name="Hanging_20_indent">')
        return characterMapping

    def get_locationMapping(self, crId):
        """Return a mapping dictionary for a location section. 
        """
        locationMapping = OdtFile.get_locationMapping(self, crId)
        locationMapping['Scenes'] = locationMapping['Scenes'].replace(
            '\n', '</text:p><text:p text:style-name="Hanging_20_indent">')
        return locationMapping

    def get_itemMapping(self, crId):
        """Return a mapping dictionary for a item section. 
        """
        itemMapping = OdtFile.get_itemMapping(self, crId)
        itemMapping['Scenes'] = itemMapping['Scenes'].replace(
            '\n', '</text:p><text:p text:style-name="Hanging_20_indent">')
        return itemMapping
