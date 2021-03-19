"""OdtXref - Class for OpenDocument xml file generation.

Create cross reference lists.

Part of the PyWriter project.
Copyright (c) 2021 Peter Triesberger
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
    characterTagsTemplate = '''<text:h text:style-name="Heading_20_2" text:outline-level="2">Characters tagged $Tag:</text:h><text:p text:style-name="Hanging_20_indent">$Elements</text:p>
'''
    locationTagsTemplate = '''<text:h text:style-name="Heading_20_2" text:outline-level="2">Locations tagged $Tag:</text:h><text:p text:style-name="Hanging_20_indent">$Elements</text:p>
'''
    itemTagsTemplate = '''<text:h text:style-name="Heading_20_2" text:outline-level="2">Items tagged $Tag:</text:h><text:p text:style-name="Hanging_20_indent">$Elements</text:p>
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

    def get_locationMapping(self, lcId):
        """Return a mapping dictionary for a location section. 
        """
        locationMapping = OdtFile.get_locationMapping(self, lcId)
        locationMapping['Scenes'] = locationMapping['Scenes'].replace(
            '\n', '</text:p><text:p text:style-name="Hanging_20_indent">')
        return locationMapping

    def get_itemMapping(self, itId):
        """Return a mapping dictionary for a item section. 
        """
        itemMapping = OdtFile.get_itemMapping(self, itId)
        itemMapping['Scenes'] = itemMapping['Scenes'].replace(
            '\n', '</text:p><text:p text:style-name="Hanging_20_indent">')
        return itemMapping

    def get_tagMapping(self, tag, xref, elements):
        """Return a mapping dictionary for a tag section. 
        """
        tagMapping = OdtFile.get_tagMapping(self, tag, xref, elements)
        tagMapping['Elements'] = tagMapping['Elements'].replace(
            '\n', '</text:p><text:p text:style-name="Hanging_20_indent">')
        return tagMapping
