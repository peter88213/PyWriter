"""CrossReferences - Class for cross reference generation.

Create dictiionaries containing a novel's cross references.

Part of the PyWriter project.
Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""


class CrossReferences():

    def __init__(self):
        # Cross reference dictionaries:

        self.scnPerChr = {}
        # Scenes per character

        self.scnPerLoc = {}
        # Scenes per location

        self.scnPerItm = {}
        # Scenes per item

        self.scnPerTag = {}
        # Scenes per tag

        self.chrPerTag = {}
        # Characters per tag

        self.locPerTag = {}
        # Locations per tag

        self.itmPerTag = {}
        # Items per tag

    def generate_xref(self, novel):
        """Generate cross references
        """
        self.scnPerChr = {}
        self.scnPerLoc = {}
        self.scnPerItm = {}
        self.scnPerTag = {}
        self.chrPerTag = {}
        self.locPerTag = {}
        self.itmPerTag = {}

        # Characters per tag:

        for crId in novel.srtCharacters:
            self.scnPerChr[crId] = []

            if novel.characters[crId].tags:

                for tag in novel.characters[crId].tags:

                    if not tag in self.chrPerTag:
                        self.chrPerTag[tag] = []

                    self.chrPerTag[tag].append(crId)

        # Locations per tag:

        for lcId in novel.srtLocations:
            self.scnPerLoc[lcId] = []

            if novel.locations[lcId].tags:

                for tag in novel.locations[lcId].tags:

                    if not tag in self.locPerTag:
                        self.locPerTag[tag] = []

                    self.locPerTag[tag].append(lcId)

        # Items per tag:

        for itId in novel.srtItems:
            self.scnPerItm[itId] = []

            if novel.items[itId].tags:

                for tag in novel.items[itId].tags:

                    if not tag in self.itmPerTag:
                        self.itmPerTag[tag] = []

                    self.itmPerTag[tag].append(itId)

        for chId in novel.srtChapters:

            for scId in novel.chapters[chId].srtScenes:

                # Scenes per character:

                if novel.scenes[scId].characters:

                    for crId in novel.scenes[scId].characters:
                        self.scnPerChr[crId].append(scId)

                # Scenes per location:

                if novel.scenes[scId].locations:

                    for lcId in novel.scenes[scId].locations:
                        self.scnPerLoc[lcId].append(scId)

                # Scenes per item:

                if novel.scenes[scId].items:

                    for itId in novel.scenes[scId].items:
                        self.scnPerItm[itId].append(scId)

                # Scenes per tag:

                if novel.scenes[scId].tags:

                    for tag in novel.scenes[scId].tags:

                        if not tag in self.scnPerTag:
                            self.scnPerTag[tag] = []

                        self.scnPerTag[tag].append(scId)
