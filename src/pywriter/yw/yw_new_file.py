"""yWNewFile - Class for yWriter xml file creation.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import xml.etree.ElementTree as ET

from pywriter.yw.yw_file import YwFile


class YwNewFile(YwFile):
    """yWriter xml project file representation."""

    def write(self):
        """Open the yWriter xml file located at filePath and 
        replace a set of attributes not being None.
        Return a message beginning with SUCCESS or ERROR.
        """

        root = ET.Element('YWRITER7')

        # Write attributes at novel level to the xml element tree.

        prj = ET.SubElement(root, 'PROJECT')
        ET.SubElement(prj, 'Ver').text = '7'

        if self.title is not None:
            ET.SubElement(prj, 'Title').text = self.title

        if self.desc is not None:
            ET.SubElement(prj, 'Desc').text = self.desc

        if self.author is not None:
            ET.SubElement(prj, 'AuthorName').text = self.author

        if self.fieldTitle1 is not None:
            ET.SubElement(prj, 'FieldTitle1').text = self.fieldTitle1

        if self.fieldTitle2 is not None:
            ET.SubElement(prj, 'FieldTitle2').text = self.fieldTitle2

        if self.fieldTitle3 is not None:
            ET.SubElement(prj, 'FieldTitle3').text = self.fieldTitle3

        if self.fieldTitle4 is not None:
            ET.SubElement(prj, 'FieldTitle4').text = self.fieldTitle4

        # Write locations to the xml element tree.

        locations = ET.SubElement(root, 'LOCATIONS')

        for lcId in self.locations:
            loc = ET.SubElement(locations, 'LOCATION')
            ET.SubElement(loc, 'ID').text = lcId

            if self.locations[lcId].title is not None:
                ET.SubElement(loc, 'Title').text = self.locations[lcId].title

            if self.locations[lcId].desc is not None:
                ET.SubElement(loc, 'Desc').text = self.locations[lcId].desc

            if self.locations[lcId].aka is not None:
                ET.SubElement(loc, 'AKA').text = self.locations[lcId].aka

            if self.locations[lcId].tags is not None:
                ET.SubElement(loc, 'Tags').text = ';'.join(
                    self.locations[lcId].tags)

        # Write items to the xml element tree.

        items = ET.SubElement(root, 'ITEMS')

        for itId in self.items:
            itm = ET.SubElement(items, 'ITEM')
            ET.SubElement(itm, 'ID').text = itId

            if self.items[itId].title is not None:
                ET.SubElement(itm, 'Title').text = self.items[itId].title

            if self.items[itId].desc is not None:
                ET.SubElement(itm, 'Desc').text = self.items[itId].desc

            if self.items[itId].aka is not None:
                ET.SubElement(itm, 'AKA').text = self.items[itId].aka

            if self.items[itId].tags is not None:
                ET.SubElement(itm, 'Tags').text = ';'.join(
                    self.items[itId].tags)

        # Write characters to the xml element tree.

        characters = ET.SubElement(root, 'CHARACTERS')

        for crId in self.characters:
            crt = ET.SubElement(characters, 'CHARACTER')
            ET.SubElement(crt, 'ID').text = crId

            if self.characters[crId].title is not None:
                ET.SubElement(
                    crt, 'Title').text = self.characters[crId].title

            if self.characters[crId].desc is not None:
                ET.SubElement(
                    crt, 'Desc').text = self.characters[crId].desc

            if self.characters[crId].aka is not None:
                ET.SubElement(crt, 'AKA').text = self.characters[crId].aka

            if self.characters[crId].tags is not None:
                ET.SubElement(crt, 'Tags').text = ';'.join(
                    self.characters[crId].tags)

            if self.characters[crId].notes is not None:
                ET.SubElement(
                    crt, 'Notes').text = self.characters[crId].notes

            if self.characters[crId].bio is not None:
                ET.SubElement(crt, 'Bio').text = self.characters[crId].bio

            if self.characters[crId].goals is not None:
                ET.SubElement(
                    crt, 'Goals').text = self.characters[crId].goals

            if self.characters[crId].fullName is not None:
                ET.SubElement(
                    crt, 'FullName').text = self.characters[crId].fullName

            if self.characters[crId].isMajor:
                ET.SubElement(crt, 'Major').text = '-1'

        # Write attributes at scene level to the xml element tree.

        scenes = ET.SubElement(root, 'SCENES')

        for scId in self.scenes:
            scn = ET.SubElement(scenes, 'SCENE')
            ET.SubElement(scn, 'ID').text = scId

            if self.scenes[scId].title is not None:
                ET.SubElement(scn, 'Title').text = self.scenes[scId].title

            for chId in self.chapters:

                if scId in self.chapters[chId].srtScenes:
                    ET.SubElement(scn, 'BelongsToChID').text = chId
                    break

            if self.scenes[scId].desc is not None:
                ET.SubElement(scn, 'Desc').text = self.scenes[scId].desc

            if self.scenes[scId].sceneContent is not None:
                ET.SubElement(scn,
                              'SceneContent').text = self.scenes[scId].sceneContent
                ET.SubElement(scn, 'WordCount').text = str(
                    self.scenes[scId].wordCount)
                ET.SubElement(scn, 'LetterCount').text = str(
                    self.scenes[scId].letterCount)

            if self.scenes[scId].isUnused:
                ET.SubElement(scn, 'Unused').text = '-1'

            scFields = ET.SubElement(scn, 'Fields')

            if self.scenes[scId].isNotesScene:
                ET.SubElement(scFields, 'Field_SceneType').text = '1'

            elif self.scenes[scId].isTodoScene:
                ET.SubElement(scFields, 'Field_SceneType').text = '2'

            if self.scenes[scId].status is not None:
                ET.SubElement(scn, 'Status').text = str(
                    self.scenes[scId].status)

            if self.scenes[scId].sceneNotes is not None:
                ET.SubElement(scn, 'Notes').text = self.scenes[scId].sceneNotes

            if self.scenes[scId].tags is not None:
                ET.SubElement(scn, 'Tags').text = ';'.join(
                    self.scenes[scId].tags)

            if self.scenes[scId].field1 is not None:
                ET.SubElement(scn, 'Field1').text = self.scenes[scId].field1

            if self.scenes[scId].field2 is not None:
                ET.SubElement(scn, 'Field2').text = self.scenes[scId].field2

            if self.scenes[scId].field3 is not None:
                ET.SubElement(scn, 'Field3').text = self.scenes[scId].field3

            if self.scenes[scId].field4 is not None:
                ET.SubElement(scn, 'Field4').text = self.scenes[scId].field4

            if self.scenes[scId].appendToPrev:
                ET.SubElement(scn, 'AppendToPrev').text = '-1'

            # Date/time information

            if (self.scenes[scId].date is not None) and (self.scenes[scId].time is not None):
                dateTime = ' '.join(
                    self.scenes[scId].date, self.scenes[scId].time)
                ET.SubElement(scn, 'SpecificDateTime').text = dateTime
                ET.SubElement(scn, 'SpecificDateMode').text = '-1'

            elif (self.scenes[scId].day is not None) or (self.scenes[scId].hour is not None) or (self.scenes[scId].minute is not None):

                if self.scenes[scId].day is not None:
                    ET.SubElement(scn, 'Day').text = self.scenes[scId].day

                if self.scenes[scId].hour is not None:
                    ET.SubElement(scn, 'Hour').text = self.scenes[scId].hour

                if self.scenes[scId].minute is not None:
                    ET.SubElement(
                        scn, 'Minute').text = self.scenes[scId].minute

            if self.scenes[scId].lastsDays is not None:
                ET.SubElement(
                    scn, 'LastsDays').text = self.scenes[scId].lastsDays

            if self.scenes[scId].lastsHours is not None:
                ET.SubElement(
                    scn, 'LastsHours').text = self.scenes[scId].lastsHours

            if self.scenes[scId].lastsMinutes is not None:
                ET.SubElement(
                    scn, 'LastsMinutes').text = self.scenes[scId].lastsMinutes

            # Plot related information

            if self.scenes[scId].isReactionScene:
                ET.SubElement(scn, 'ReactionScene').text = '-1'

            if self.scenes[scId].isSubPlot:
                ET.SubElement(scn, 'SubPlot').text = '-1'

            if self.scenes[scId].goal is not None:
                ET.SubElement(scn, 'Goal').text = self.scenes[scId].goal

            if self.scenes[scId].conflict is not None:
                ET.SubElement(
                    scn, 'Conflict').text = self.scenes[scId].conflict

            if self.scenes[scId].outcome is not None:
                ET.SubElement(scn, 'Outcome').text = self.scenes[scId].outcome

            if self.scenes[scId].characters is not None:
                scCharacters = ET.SubElement(scn, 'Characters')

                for crId in self.scenes[scId].characters:
                    ET.SubElement(scCharacters, 'CharID').text = crId

            if self.scenes[scId].locations is not None:
                scLocations = ET.SubElement(scn, 'Locations')

                for lcId in self.scenes[scId].locations:
                    ET.SubElement(scLocations, 'LocID').text = lcId

            if self.scenes[scId].items is not None:
                scItems = ET.SubElement(scn, 'Items')

                for itId in self.scenes[scId].items:
                    ET.SubElement(scItems, 'ItemID').text = itId

        # Write attributes at chapter level to the xml element tree.

        chapters = ET.SubElement(root, 'CHAPTERS')

        sortOrder = 0

        for chId in self.srtChapters:
            sortOrder += 1
            chp = ET.SubElement(chapters, 'CHAPTER')
            ET.SubElement(chp, 'ID').text = chId
            ET.SubElement(chp, 'SortOrder').text = str(sortOrder)

            if self.chapters[chId].title is not None:
                ET.SubElement(chp, 'Title').text = self.chapters[chId].title

            if self.chapters[chId].desc is not None:
                ET.SubElement(chp, 'Desc').text = self.chapters[chId].desc

            if self.chapters[chId].chLevel == 1:
                ET.SubElement(chp, 'SectionStart').text = '-1'

            if self.chapters[chId].oldType is not None:
                ET.SubElement(chp, 'Type').text = str(
                    self.chapters[chId].oldType)

            if self.chapters[chId].chType is not None:
                ET.SubElement(chp, 'ChapterType').text = str(
                    self.chapters[chId].chType)

            if self.chapters[chId].isUnused:
                ET.SubElement(chp, 'Unused').text = '-1'

            sortSc = ET.SubElement(chp, 'Scenes')

            for scId in self.chapters[chId].srtScenes:
                ET.SubElement(sortSc, 'ScID').text = scId

            chFields = ET.SubElement(chp, 'Fields')

            if self.chapters[chId].title.startswith('@'):
                self.chapters[chId].suppressChapterTitle = True

            if self.chapters[chId].suppressChapterTitle:
                ET.SubElement(
                    chFields, 'Field_SuppressChapterTitle').text = '1'

        # Save the xml tree in a file.

        self.ywTreeBuilder.indent_xml(root)

        self._tree = ET.ElementTree(root)

        message = self.ywTreeWriter.write_element_tree(self)

        if message.startswith('ERROR'):
            return message

        message = self.ywPostprocessor.postprocess_xml_file(self.filePath)

        if message.startswith('ERROR'):
            return message

        return 'SUCCESS: project data written to "' + self._filePath + '".'
