"""Provide a class for ODT cross reference export.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from string import Template

from pywriter.model.cross_references import CrossReferences
from pywriter.odt.odt_file import OdtFile


class OdtXref(OdtFile):
    """OpenDocument xml cross reference file representation."""

    DESCRIPTION = 'Cross reference'
    SUFFIX = '_xref'

    fileHeader = OdtFile.CONTENT_XML_HEADER + '''<text:p text:style-name="Title">$Title</text:p>
<text:p text:style-name="Subtitle">$AuthorName</text:p>
'''
    sceneTemplate = '''<text:p text:style-name="yWriter_20_mark">
<text:a xlink:href="../${ProjectName}_manuscript.odt#ScID:$ID%7Cregion">$SceneNumber</text:a> (Ch $Chapter) $Title
</text:p>
'''
    unusedSceneTemplate = '''<text:p text:style-name="yWriter_20_mark_20_unused">
$SceneNumber (Ch $Chapter) $Title (Unused)
</text:p>
'''
    notesSceneTemplate = '''<text:p text:style-name="yWriter_20_mark_20_notes">
$SceneNumber (Ch $Chapter) $Title (Notes)
</text:p>
'''
    todoSceneTemplate = '''<text:p text:style-name="yWriter_20_mark_20_todo">
$SceneNumber (Ch $Chapter) $Title (ToDo)
</text:p>
'''
    characterTemplate = '''<text:p text:style-name="Text_20_body">
<text:a xlink:href="../${ProjectName}_characters.odt#CrID:$ID%7Cregion">$Title</text:a> $FullName
</text:p>
'''
    locationTemplate = '''<text:p text:style-name="Text_20_body">
<text:a xlink:href="../${ProjectName}_locations.odt#LcID:$ID%7Cregion">$Title</text:a>
</text:p>
'''
    itemTemplate = '''<text:p text:style-name="Text_20_body">
<text:a xlink:href="../${ProjectName}_items.odt#ItrID:$ID%7Cregion">$Title</text:a>
</text:p>
'''
    scnPerChrTemplate = '''<text:h text:style-name="Heading_20_2" text:outline-level="2">Scenes with Character $Title:</text:h>
'''
    scnPerLocTemplate = '''<text:h text:style-name="Heading_20_2" text:outline-level="2">Scenes with Location $Title:</text:h>
'''
    scnPerItmTemplate = '''<text:h text:style-name="Heading_20_2" text:outline-level="2">Scenes with Item $Title:</text:h>
'''
    chrPerTagTemplate = '''<text:h text:style-name="Heading_20_2" text:outline-level="2">Characters tagged $Tag:</text:h>
'''
    locPerTagTemplate = '''<text:h text:style-name="Heading_20_2" text:outline-level="2">Locations tagged $Tag:</text:h>
'''
    itmPerTagTemplate = '''<text:h text:style-name="Heading_20_2" text:outline-level="2">Items tagged $Tag:</text:h>
'''
    scnPerTagtemplate = '''<text:h text:style-name="Heading_20_2" text:outline-level="2">Scenes tagged $Tag:</text:h>
'''
    fileFooter = OdtFile.CONTENT_XML_FOOTER

    def __init__(self, filePath, **kwargs):
        """Apply the strategy pattern 
        by delegating the cross reference to an external object.
        """
        OdtFile.__init__(self, filePath)
        self.xr = CrossReferences()

    def get_sceneMapping(self, scId):
        """Add the chapter number to the original mapping dictionary.
        """
        sceneNumber = self.xr.srtScenes.index(scId) + 1
        sceneMapping = OdtFile.get_sceneMapping(self, scId, sceneNumber, 0, 0)
        chapterNumber = self.srtChapters.index(self.xr.chpPerScn[scId]) + 1
        sceneMapping['Chapter'] = str(chapterNumber)
        return sceneMapping

    def get_tagMapping(self, tag):
        """Return a mapping dictionary for a tags section. 
        """
        tagMapping = dict(
            Tag=tag,
        )
        return tagMapping

    def get_scenes(self, scenes):
        """Process the scenes.
        Return a list of strings.
        Override the superclass method.
        """
        lines = []

        for scId in scenes:

            if self.scenes[scId].isNotesScene:
                template = Template(self.notesSceneTemplate)

            elif self.scenes[scId].isTodoScene:
                template = Template(self.todoSceneTemplate)

            elif self.scenes[scId].isUnused:
                template = Template(self.unusedSceneTemplate)

            else:
                template = Template(self.sceneTemplate)

            lines.append(template.safe_substitute(
                self.get_sceneMapping(scId)))

        return lines

    def get_sceneTags(self):
        """Process the scene related tags.
        Return a list of strings.
        """
        lines = []
        headerTemplate = Template(self.scnPerTagtemplate)

        for tag in self.xr.scnPerTag:

            if self.xr.scnPerTag[tag] != []:
                lines.append(headerTemplate.safe_substitute(
                    self.get_tagMapping(tag)))
                lines.extend(self.get_scenes(self.xr.scnPerTag[tag]))

        return lines

    def get_characters(self):
        """Process the scenes per character.
        Return a list of strings.
        Override the superclass method.
        """
        lines = []
        headerTemplate = Template(self.scnPerChrTemplate)

        for crId in self.xr.scnPerChr:

            if self.xr.scnPerChr[crId] != []:
                lines.append(headerTemplate.safe_substitute(
                    self.get_characterMapping(crId)))
                lines.extend(self.get_scenes(self.xr.scnPerChr[crId]))

        return lines

    def get_locations(self):
        """Process the locations.
        Return a list of strings.
        Override the superclass method.
        """
        lines = []
        headerTemplate = Template(self.scnPerLocTemplate)

        for lcId in self.xr.scnPerLoc:

            if self.xr.scnPerLoc[lcId] != []:
                lines.append(headerTemplate.safe_substitute(
                    self.get_locationMapping(lcId)))
                lines.extend(self.get_scenes(self.xr.scnPerLoc[lcId]))

        return lines

    def get_items(self):
        """Process the items.
        Return a list of strings.
        Override the superclass method.
        """
        lines = []
        headerTemplate = Template(self.scnPerItmTemplate)

        for itId in self.xr.scnPerItm:

            if self.xr.scnPerItm[itId] != []:
                lines.append(headerTemplate.safe_substitute(
                    self.get_itemMapping(itId)))
                lines.extend(self.get_scenes(self.xr.scnPerItm[itId]))

        return lines

    def get_characterTags(self):
        """Process the character related tags.
        Return a list of strings.
        """
        lines = []
        headerTemplate = Template(self.chrPerTagTemplate)
        template = Template(self.characterTemplate)

        for tag in self.xr.chrPerTag:

            if self.xr.chrPerTag[tag] != []:
                lines.append(headerTemplate.safe_substitute(
                    self.get_tagMapping(tag)))

                for crId in self.xr.chrPerTag[tag]:
                    lines.append(template.safe_substitute(
                        self.get_characterMapping(crId)))

        return lines

    def get_locationTags(self):
        """Process the location related tags.
        Return a list of strings.
        """
        lines = []
        headerTemplate = Template(self.locPerTagTemplate)
        template = Template(self.locationTemplate)

        for tag in self.xr.locPerTag:

            if self.xr.locPerTag[tag]:
                lines.append(headerTemplate.safe_substitute(
                    self.get_tagMapping(tag)))

                for lcId in self.xr.locPerTag[tag]:
                    lines.append(template.safe_substitute(
                        self.get_locationMapping(lcId)))

        return lines

    def get_itemTags(self):
        """Process the item related tags.
        Return a list of strings.
        """
        lines = []
        headerTemplate = Template(self.itmPerTagTemplate)
        template = Template(self.itemTemplate)

        for tag in self.xr.itmPerTag:

            if self.xr.itmPerTag[tag] != []:
                lines.append(headerTemplate.safe_substitute(
                    self.get_tagMapping(tag)))

                for itId in self.xr.itmPerTag[tag]:
                    lines.append(template.safe_substitute(
                        self.get_itemMapping(itId)))

        return lines

    def get_text(self):
        """Assemple the whole text applying the templates.
        Return a string to be written to the output file.
        Override the superclass method.
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
