"""OdtXref - Class for OpenDocument xml file generation.

Create ODT document containing ross references.

Part of the PyWriter project.
Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from string import Template

from pywriter.model.cross_references import CrossReferences
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
    sceneTagsTemplate = '''<text:h text:style-name="Heading_20_2" text:outline-level="2">Scenes tagged $Tag:</text:h><text:p text:style-name="Hanging_20_indent">$Elements</text:p>
'''
    fileFooter = OdtFile.CONTENT_XML_FOOTER

    def __init__(self, filePath):
        """Apply the strategy pattern 
        by delegating the cross reference to an external object.
        """
        OdtFile.__init__(self, filePath)
        self.xr = CrossReferences()

    def get_characterMapping(self, crId):
        """Return a mapping dictionary for a character section.
        Add character-related scenes ($Scenes) to the dictionary.
        """
        characterMapping = OdtFile.get_characterMapping(self, crId)

        if self.xr.scnPerChr[crId]:
            substitutes = []

            for scId in self.xr.scnPerChr[crId]:
                substitutes.append(self.scenes[scId].title)

            characterMapping['Scenes'] = '</text:p><text:p text:style-name="Hanging_20_indent">'.join(
                substitutes)

        else:
            characterMapping['Scenes'] = ''

        return characterMapping

    def get_locationMapping(self, lcId):
        """Return a mapping dictionary for a location section. 
        Add location-related scenes ($Scenes) to the dictionary.
        """
        locationMapping = OdtFile.get_locationMapping(self, lcId)

        if self.xr.scnPerLoc[lcId]:
            substitutes = []

            for scId in self.xr.scnPerLoc[lcId]:
                substitutes.append(self.scenes[scId].title)

            locationMapping['Scenes'] = '</text:p><text:p text:style-name="Hanging_20_indent">'.join(
                substitutes)

        else:
            locationMapping['Scenes'] = ''

        return locationMapping

    def get_itemMapping(self, itId):
        """Return a mapping dictionary for a item section. 
        Add item-related scenes ($Scenes) to the dictionary.
        """
        itemMapping = OdtFile.get_itemMapping(self, itId)

        if self.xr.scnPerItm[itId]:
            substitutes = []

            for scId in self.xr.scnPerItm[itId]:
                substitutes.append(self.scenes[scId].title)

            itemMapping['Scenes'] = '</text:p><text:p text:style-name="Hanging_20_indent">'.join(
                substitutes)

        else:
            itemMapping['Scenes'] = ''

        return itemMapping

    def get_tagMapping(self, tag, xref, elements):
        """Return a mapping dictionary for a tags section. 
        xref: Cross reference dictionary.
        elements: dictionary of tagged elements.
        """

        try:
            titlelist = []

            for elementId in xref:
                titlelist.append(elements[elementId].title)

            titles = '</text:p><text:p text:style-name="Hanging_20_indent">'.join(
                titlelist)

        except:
            titles = ''

        tagMapping = dict(
            Tag=tag,
            Elements=titles,
        )
        return tagMapping

    def get_sceneTags(self):
        """Process the scene related tags.
        Return a list of strings.
        """
        lines = []

        for tag in self.xr.scnPerTag:
            template = Template(self.sceneTagsTemplate)
            lines.append(template.safe_substitute(
                self.get_tagMapping(tag, self.xr.scnPerTag[tag], self.scenes)))

        return lines

    def get_characterTags(self):
        """Process the character related tags.
        Return a list of strings.
        """
        lines = []

        for tag in self.xr.chrPerTag:
            template = Template(self.characterTagsTemplate)
            lines.append(template.safe_substitute(
                self.get_tagMapping(tag, self.xr.chrPerTag[tag], self.characters)))

        return lines

    def get_locationTags(self):
        """Process the location related tags.
        Return a list of strings.
        """
        lines = []

        for tag in self.xr.locPerTag:
            template = Template(self.locationTagsTemplate)
            lines.append(template.safe_substitute(
                self.get_tagMapping(tag, self.xr.locPerTag[tag], self.locations)))

        return lines

    def get_itemTags(self):
        """Process the item related tags.
        Return a list of strings.
        """
        lines = []

        for tag in self.xr.itmPerTag:
            template = Template(self.itemTagsTemplate)
            lines.append(template.safe_substitute(
                self.get_tagMapping(tag, self.xr.itmPerTag[tag], self.items)))

        return lines

    def get_text(self):
        """Apply the template method pattern
        by overwriting a method called during the file export process.
        """
        self.xr.generate_xref(self)

        lines = self.get_fileHeader()
        lines.extend(self.get_characters())
        lines.extend(self.get_locations())
        lines.extend(self.get_items())
        lines.extend(self.get_sceneTags())
        lines.extend(self.get_characterTags())
        lines.extend(self.get_locationTags())
        lines.extend(self.get_itemTags())
        lines.append(self.fileFooter)
        return ''.join(lines)
