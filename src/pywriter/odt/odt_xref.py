"""OdtXref - Class for OpenDocument xml file generation.

Create cross reference lists.

Part of the PyWriter project.
Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from string import Template

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
        OdtFile.__init__(self, filePath)

        # Cross reference dictionaries:

        self.chrScnXref = {}
        # Scenes per character

        self.locScnXref = {}
        # Scenes per location

        self.itmScnXref = {}
        # Scenes per item

        self.tagsScXref = {}
        # Scenes per tag

        self.tagsCrXref = {}
        # Characters per tag

        self.tagsLcXref = {}
        # Locations per tag

        self.tagsItXref = {}
        # Items per tag

    def make_xref(self):
        """Generate cross references
        """
        self.chrScnXref = {}
        self.locScnXref = {}
        self.itmScnXref = {}
        self.tagsScXref = {}
        self.tagsCrXref = {}
        self.tagsLcXref = {}
        self.tagsItXref = {}

        # Characters per tag:

        for crId in self.srtCharacters:
            self.chrScnXref[crId] = []

            if self.characters[crId].tags:

                for tag in self.characters[crId].tags:

                    if not tag in self.tagsCrXref:
                        self.tagsCrXref[tag] = []

                    self.tagsCrXref[tag].append(crId)

        # Locations per tag:

        for lcId in self.srtLocations:
            self.locScnXref[lcId] = []

            if self.locations[lcId].tags:

                for tag in self.locations[lcId].tags:

                    if not tag in self.tagsLcXref:
                        self.tagsLcXref[tag] = []

                    self.tagsLcXref[tag].append(lcId)

        # Items per tag:

        for itId in self.srtItems:
            self.itmScnXref[itId] = []

            if self.items[itId].tags:

                for tag in self.items[itId].tags:

                    if not tag in self.tagsItXref:
                        self.tagsItXref[tag] = []

                    self.tagsItXref[tag].append(itId)

        for chId in self.srtChapters:

            for scId in self.chapters[chId].srtScenes:

                # Scenes per character:

                if self.scenes[scId].characters:

                    for crId in self.scenes[scId].characters:
                        self.chrScnXref[crId].append(scId)

                # Scenes per location:

                if self.scenes[scId].locations:

                    for lcId in self.scenes[scId].locations:
                        self.locScnXref[lcId].append(scId)

                # Scenes per item:

                if self.scenes[scId].items:

                    for itId in self.scenes[scId].items:
                        self.itmScnXref[itId].append(scId)

                # Scenes per tag:

                if self.scenes[scId].tags:

                    for tag in self.scenes[scId].tags:

                        if not tag in self.tagsScXref:
                            self.tagsScXref[tag] = []

                        self.tagsScXref[tag].append(scId)

    def get_characterMapping(self, crId):
        """Return a mapping dictionary for a character section.
        Add character-related scenes ($Scenes) to the dictionary.
        """
        characterMapping = OdtFile.get_characterMapping(self, crId)

        if self.chrScnXref[crId]:
            substitutes = []

            for scId in self.chrScnXref[crId]:
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

        if self.locScnXref[lcId]:
            substitutes = []

            for scId in self.locScnXref[lcId]:
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

        if self.itmScnXref[itId]:
            substitutes = []

            for scId in self.itmScnXref[itId]:
                substitutes.append(self.scenes[scId].title)

            itemMapping['Scenes'] = '</text:p><text:p text:style-name="Hanging_20_indent">'.join(
                substitutes)

        else:
            itemMapping['Scenes'] = ''

        return itemMapping

    def get_tagMapping(self, tag, xref, elements):
        """Return a mapping dictionary for a tag section. 
        """
        tagMapping = OdtFile.get_tagMapping(self, tag, xref, elements)
        tagMapping['Elements'] = tagMapping['Elements'].replace(
            '\n', '</text:p><text:p text:style-name="Hanging_20_indent">')
        return tagMapping

    def get_sceneTags(self):
        """Process the scene related tags.
        Return a list of strings.
        """
        lines = []

        for tag in self.tagsScXref:
            template = Template(self.sceneTagsTemplate)
            lines.append(template.safe_substitute(
                self.get_tagMapping(tag, self.tagsScXref[tag], self.scenes)))

        return lines

    def get_characterTags(self):
        """Process the character related tags.
        Return a list of strings.
        """
        lines = []

        for tag in self.tagsCrXref:
            template = Template(self.characterTagsTemplate)
            lines.append(template.safe_substitute(
                self.get_tagMapping(tag, self.tagsCrXref[tag], self.characters)))

        return lines

    def get_locationTags(self):
        """Process the location related tags.
        Return a list of strings.
        """
        lines = []

        for tag in self.tagsLcXref:
            template = Template(self.locationTagsTemplate)
            lines.append(template.safe_substitute(
                self.get_tagMapping(tag, self.tagsLcXref[tag], self.locations)))

        return lines

    def get_itemTags(self):
        """Process the item related tags.
        Return a list of strings.
        """
        lines = []

        for tag in self.tagsItXref:
            template = Template(self.itemTagsTemplate)
            lines.append(template.safe_substitute(
                self.get_tagMapping(tag, self.tagsItXref[tag], self.items)))

        return lines

    def get_text(self):
        """Assemple the whole text applying the templates.
        Return a string to be written to the output file.
        """
        self.make_xref()
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
