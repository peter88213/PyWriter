"""Build yWriter project xml tree.

Part of the PyWriter project.
Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import xml.etree.ElementTree as ET

from abc import abstractmethod


class YwTreeBuilder():
    """Build yWriter project xml tree."""

    @abstractmethod
    def build_element_tree(self, ywProject):
        """Modify the yWriter project attributes of an existing xml element tree.
        Return a message beginning with SUCCESS or ERROR.
        To be overwritten by file format specific subclasses.
        """
        root = ywProject._tree.getroot()

        # Write locations to the xml element tree.

        locations = root.find('LOCATIONS')
        sortOrder = 0

        # Remove LOCATION entries in order to rewrite
        # the LOCATIONS section in a modified sort order.

        for loc in locations.findall('LOCATION'):
            locations.remove(loc)

        for lcId in ywProject.srtLocations:
            loc = ET.SubElement(locations, 'LOCATION')
            ET.SubElement(loc, 'ID').text = lcId

            if ywProject.locations[lcId].title is not None:
                ET.SubElement(
                    loc, 'Title').text = ywProject.locations[lcId].title

            if ywProject.locations[lcId].image is not None:
                ET.SubElement(
                    loc, 'ImageFile').text = ywProject.locations[lcId].image

            if ywProject.locations[lcId].desc is not None:
                ET.SubElement(
                    loc, 'Desc').text = ywProject.locations[lcId].desc

            if ywProject.locations[lcId].aka is not None:
                ET.SubElement(loc, 'AKA').text = ywProject.locations[lcId].aka

            if ywProject.locations[lcId].tags is not None:
                ET.SubElement(loc, 'Tags').text = ';'.join(
                    ywProject.locations[lcId].tags)

            sortOrder += 1
            ET.SubElement(loc, 'SortOrder').text = str(sortOrder)

        # Write items to the xml element tree.

        items = root.find('ITEMS')
        sortOrder = 0

        # Remove ITEM entries in order to rewrite
        # the ITEMS section in a modified sort order.

        for itm in items.findall('ITEM'):
            items.remove(itm)

        for itId in ywProject.srtItems:
            itm = ET.SubElement(items, 'ITEM')
            ET.SubElement(itm, 'ID').text = itId

            if ywProject.items[itId].title is not None:
                ET.SubElement(itm, 'Title').text = ywProject.items[itId].title

            if ywProject.items[itId].image is not None:
                ET.SubElement(
                    itm, 'ImageFile').text = ywProject.items[itId].image

            if ywProject.items[itId].desc is not None:
                ET.SubElement(itm, 'Desc').text = ywProject.items[itId].desc

            if ywProject.items[itId].aka is not None:
                ET.SubElement(itm, 'AKA').text = ywProject.items[itId].aka

            if ywProject.items[itId].tags is not None:
                ET.SubElement(itm, 'Tags').text = ';'.join(
                    ywProject.items[itId].tags)

            sortOrder += 1
            ET.SubElement(itm, 'SortOrder').text = str(sortOrder)

        # Write characters to the xml element tree.

        characters = root.find('CHARACTERS')
        sortOrder = 0

        # Remove CHARACTER entries in order to rewrite
        # the CHARACTERS section in a modified sort order.

        for crt in characters.findall('CHARACTER'):
            characters.remove(crt)

        for crId in ywProject.srtCharacters:
            crt = ET.SubElement(characters, 'CHARACTER')
            ET.SubElement(crt, 'ID').text = crId

            if ywProject.characters[crId].title is not None:
                ET.SubElement(
                    crt, 'Title').text = ywProject.characters[crId].title

            if ywProject.characters[crId].desc is not None:
                ET.SubElement(
                    crt, 'Desc').text = ywProject.characters[crId].desc

            if ywProject.characters[crId].image is not None:
                ET.SubElement(
                    crt, 'ImageFile').text = ywProject.characters[crId].image

            sortOrder += 1
            ET.SubElement(crt, 'SortOrder').text = str(sortOrder)

            if ywProject.characters[crId].notes is not None:
                ET.SubElement(
                    crt, 'Notes').text = ywProject.characters[crId].notes

            if ywProject.characters[crId].aka is not None:
                ET.SubElement(crt, 'AKA').text = ywProject.characters[crId].aka

            if ywProject.characters[crId].tags is not None:
                ET.SubElement(crt, 'Tags').text = ';'.join(
                    ywProject.characters[crId].tags)

            if ywProject.characters[crId].bio is not None:
                ET.SubElement(crt, 'Bio').text = ywProject.characters[crId].bio

            if ywProject.characters[crId].goals is not None:
                ET.SubElement(
                    crt, 'Goals').text = ywProject.characters[crId].goals

            if ywProject.characters[crId].fullName is not None:
                ET.SubElement(
                    crt, 'FullName').text = ywProject.characters[crId].fullName

            if ywProject.characters[crId].isMajor:
                ET.SubElement(crt, 'Major').text = '-1'

        # Write attributes at novel level to the xml element tree.

        prj = root.find('PROJECT')
        prj.find('Title').text = ywProject.title

        if ywProject.desc is not None:

            if prj.find('Desc') is None:
                ET.SubElement(prj, 'Desc').text = ywProject.desc

            else:
                prj.find('Desc').text = ywProject.desc

        if ywProject.author is not None:

            if prj.find('AuthorName') is None:
                ET.SubElement(prj, 'AuthorName').text = ywProject.author

            else:
                prj.find('AuthorName').text = ywProject.author

        prj.find('FieldTitle1').text = ywProject.fieldTitle1
        prj.find('FieldTitle2').text = ywProject.fieldTitle2
        prj.find('FieldTitle3').text = ywProject.fieldTitle3
        prj.find('FieldTitle4').text = ywProject.fieldTitle4

        # Write attributes at chapter level to the xml element tree.

        for chp in root.iter('CHAPTER'):
            chId = chp.find('ID').text

            if chId in ywProject.chapters:
                chp.find('Title').text = ywProject.chapters[chId].title

                if ywProject.chapters[chId].desc is not None:

                    if chp.find('Desc') is None:
                        ET.SubElement(
                            chp, 'Desc').text = ywProject.chapters[chId].desc

                    else:
                        chp.find('Desc').text = ywProject.chapters[chId].desc

                levelInfo = chp.find('SectionStart')

                if levelInfo is not None:

                    if ywProject.chapters[chId].chLevel == 0:
                        chp.remove(levelInfo)

                chp.find('Type').text = str(ywProject.chapters[chId].oldType)

                if ywProject.chapters[chId].chType is not None:

                    if chp.find('ChapterType') is not None:
                        chp.find('ChapterType').text = str(
                            ywProject.chapters[chId].chType)
                    else:
                        ET.SubElement(chp, 'ChapterType').text = str(
                            ywProject.chapters[chId].chType)

                if ywProject.chapters[chId].isUnused:

                    if chp.find('Unused') is None:
                        ET.SubElement(chp, 'Unused').text = '-1'

                elif chp.find('Unused') is not None:
                    chp.remove(chp.find('Unused'))

        # Write attributes at scene level to the xml element tree.

        for scn in root.iter('SCENE'):
            scId = scn.find('ID').text

            if scId in ywProject.scenes:

                if ywProject.scenes[scId].title is not None:
                    scn.find('Title').text = ywProject.scenes[scId].title

                if ywProject.scenes[scId].desc is not None:

                    if scn.find('Desc') is None:
                        ET.SubElement(
                            scn, 'Desc').text = ywProject.scenes[scId].desc

                    else:
                        scn.find('Desc').text = ywProject.scenes[scId].desc

                # Scene content is written in subclasses.

                if ywProject.scenes[scId].isUnused:

                    if scn.find('Unused') is None:
                        ET.SubElement(scn, 'Unused').text = '-1'

                elif scn.find('Unused') is not None:
                    scn.remove(scn.find('Unused'))

                if ywProject.scenes[scId].isNotesScene:

                    if scn.find('Fields') is None:
                        scFields = ET.SubElement(scn, 'Fields')

                    else:
                        scFields = scn.find('Fields')

                    if scFields.find('Field_SceneType') is None:
                        ET.SubElement(scFields, 'Field_SceneType').text = '1'

                elif scn.find('Fields') is not None:
                    scFields = scn.find('Fields')

                    if scFields.find('Field_SceneType') is not None:

                        if scFields.find('Field_SceneType').text == '1':
                            scFields.remove(scFields.find('Field_SceneType'))

                if ywProject.scenes[scId].isTodoScene:

                    if scn.find('Fields') is None:
                        scFields = ET.SubElement(scn, 'Fields')

                    else:
                        scFields = scn.find('Fields')

                    if scFields.find('Field_SceneType') is None:
                        ET.SubElement(scFields, 'Field_SceneType').text = '2'

                elif scn.find('Fields') is not None:
                    scFields = scn.find('Fields')

                    if scFields.find('Field_SceneType') is not None:

                        if scFields.find('Field_SceneType').text == '2':
                            scFields.remove(scFields.find('Field_SceneType'))

                if ywProject.scenes[scId].status is not None:
                    scn.find('Status').text = str(
                        ywProject.scenes[scId].status)

                if ywProject.scenes[scId].sceneNotes is not None:

                    if scn.find('Notes') is None:
                        ET.SubElement(
                            scn, 'Notes').text = ywProject.scenes[scId].sceneNotes

                    else:
                        scn.find(
                            'Notes').text = ywProject.scenes[scId].sceneNotes

                if ywProject.scenes[scId].tags is not None:

                    if scn.find('Tags') is None:
                        ET.SubElement(scn, 'Tags').text = ';'.join(
                            ywProject.scenes[scId].tags)

                    else:
                        scn.find('Tags').text = ';'.join(
                            ywProject.scenes[scId].tags)

                if ywProject.scenes[scId].field1 is not None:

                    if scn.find('Field1') is None:
                        ET.SubElement(
                            scn, 'Field1').text = ywProject.scenes[scId].field1

                    else:
                        scn.find('Field1').text = ywProject.scenes[scId].field1

                if ywProject.scenes[scId].field2 is not None:

                    if scn.find('Field2') is None:
                        ET.SubElement(
                            scn, 'Field2').text = ywProject.scenes[scId].field2

                    else:
                        scn.find('Field2').text = ywProject.scenes[scId].field2

                if ywProject.scenes[scId].field3 is not None:

                    if scn.find('Field3') is None:
                        ET.SubElement(
                            scn, 'Field3').text = ywProject.scenes[scId].field3

                    else:
                        scn.find('Field3').text = ywProject.scenes[scId].field3

                if ywProject.scenes[scId].field4 is not None:

                    if scn.find('Field4') is None:
                        ET.SubElement(
                            scn, 'Field4').text = ywProject.scenes[scId].field4

                    else:
                        scn.find('Field4').text = ywProject.scenes[scId].field4

                if ywProject.scenes[scId].appendToPrev:

                    if scn.find('AppendToPrev') is None:
                        ET.SubElement(scn, 'AppendToPrev').text = '-1'

                elif scn.find('AppendToPrev') is not None:
                    scn.remove(scn.find('AppendToPrev'))

                # Date/time information

                if (ywProject.scenes[scId].date is not None) and (ywProject.scenes[scId].time is not None):
                    dateTime = ywProject.scenes[scId].date + \
                        ' ' + ywProject.scenes[scId].time

                    if scn.find('SpecificDateTime') is not None:
                        scn.find('SpecificDateTime').text = dateTime

                    else:
                        ET.SubElement(scn, 'SpecificDateTime').text = dateTime
                        ET.SubElement(scn, 'SpecificDateMode').text = '-1'

                        if scn.find('Day') is not None:
                            scn.remove(scn.find('Day'))

                        if scn.find('Hour') is not None:
                            scn.remove(scn.find('Hour'))

                        if scn.find('Minute') is not None:
                            scn.remove(scn.find('Minute'))

                elif (ywProject.scenes[scId].day is not None) or (ywProject.scenes[scId].hour is not None) or (ywProject.scenes[scId].minute is not None):

                    if scn.find('SpecificDateTime') is not None:
                        scn.remove(scn.find('SpecificDateTime'))

                    if scn.find('SpecificDateMode') is not None:
                        scn.remove(scn.find('SpecificDateMode'))

                    if ywProject.scenes[scId].day is not None:

                        if scn.find('Day') is not None:
                            scn.find('Day').text = ywProject.scenes[scId].day

                        else:
                            ET.SubElement(
                                scn, 'Day').text = ywProject.scenes[scId].day

                    if ywProject.scenes[scId].hour is not None:

                        if scn.find('Hour') is not None:
                            scn.find('Hour').text = ywProject.scenes[scId].hour

                        else:
                            ET.SubElement(
                                scn, 'Hour').text = ywProject.scenes[scId].hour

                    if ywProject.scenes[scId].minute is not None:

                        if scn.find('Minute') is not None:
                            scn.find(
                                'Minute').text = ywProject.scenes[scId].minute

                        else:
                            ET.SubElement(
                                scn, 'Minute').text = ywProject.scenes[scId].minute

                if ywProject.scenes[scId].lastsDays is not None:

                    if scn.find('LastsDays') is not None:
                        scn.find(
                            'LastsDays').text = ywProject.scenes[scId].lastsDays

                    else:
                        ET.SubElement(
                            scn, 'LastsDays').text = ywProject.scenes[scId].lastsDays

                if ywProject.scenes[scId].lastsHours is not None:

                    if scn.find('LastsHours') is not None:
                        scn.find(
                            'LastsHours').text = ywProject.scenes[scId].lastsHours

                    else:
                        ET.SubElement(
                            scn, 'LastsHours').text = ywProject.scenes[scId].lastsHours

                if ywProject.scenes[scId].lastsMinutes is not None:

                    if scn.find('LastsMinutes') is not None:
                        scn.find(
                            'LastsMinutes').text = ywProject.scenes[scId].lastsMinutes

                    else:
                        ET.SubElement(
                            scn, 'LastsMinutes').text = ywProject.scenes[scId].lastsMinutes

                # Plot related information

                if ywProject.scenes[scId].isReactionScene:

                    if scn.find('ReactionScene') is None:
                        ET.SubElement(scn, 'ReactionScene').text = '-1'

                elif scn.find('ReactionScene') is not None:
                    scn.remove(scn.find('ReactionScene'))

                if ywProject.scenes[scId].isSubPlot:

                    if scn.find('SubPlot') is None:
                        ET.SubElement(scn, 'SubPlot').text = '-1'

                elif scn.find('SubPlot') is not None:
                    scn.remove(scn.find('SubPlot'))

                if ywProject.scenes[scId].goal is not None:

                    if scn.find('Goal') is None:
                        ET.SubElement(
                            scn, 'Goal').text = ywProject.scenes[scId].goal

                    else:
                        scn.find('Goal').text = ywProject.scenes[scId].goal

                if ywProject.scenes[scId].conflict is not None:

                    if scn.find('Conflict') is None:
                        ET.SubElement(
                            scn, 'Conflict').text = ywProject.scenes[scId].conflict

                    else:
                        scn.find(
                            'Conflict').text = ywProject.scenes[scId].conflict

                if ywProject.scenes[scId].outcome is not None:

                    if scn.find('Outcome') is None:
                        ET.SubElement(
                            scn, 'Outcome').text = ywProject.scenes[scId].outcome

                    else:
                        scn.find(
                            'Outcome').text = ywProject.scenes[scId].outcome

                if ywProject.scenes[scId].characters is not None:
                    characters = scn.find('Characters')

                    for oldCrId in characters.findall('CharID'):
                        characters.remove(oldCrId)

                    for crId in ywProject.scenes[scId].characters:
                        ET.SubElement(characters, 'CharID').text = crId

                if ywProject.scenes[scId].locations is not None:
                    locations = scn.find('Locations')

                    for oldLcId in locations.findall('LocID'):
                        locations.remove(oldLcId)

                    for lcId in ywProject.scenes[scId].locations:
                        ET.SubElement(locations, 'LocID').text = lcId

                if ywProject.scenes[scId].items is not None:
                    items = scn.find('Items')

                    for oldItId in items.findall('ItemID'):
                        items.remove(oldItId)

                    for itId in ywProject.scenes[scId].items:
                        ET.SubElement(items, 'ItemID').text = itId

        self.indent_xml(root)
        ywProject._tree = ET.ElementTree(root)

        return 'SUCCESS'

    def indent_xml(self, elem, level=0):
        """xml pretty printer

        Kudos to to Fredrik Lundh. 
        Source: http://effbot.org/zone/element-lib.htm#prettyprint
        """
        i = "\n" + level * "  "

        if len(elem):

            if not elem.text or not elem.text.strip():
                elem.text = i + "  "

            if not elem.tail or not elem.tail.strip():
                elem.tail = i

            for elem in elem:
                self.indent_xml(elem, level + 1)

            if not elem.tail or not elem.tail.strip():
                elem.tail = i

        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
