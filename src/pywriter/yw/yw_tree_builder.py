"""Build yWriter project xml tree.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import xml.etree.ElementTree as ET


class YwTreeBuilder():
    """Build yWriter project xml tree."""

    def build_element_tree(self, ywFile):
        """Write back the xml element tree to a yWriter xml file located at filePath.
        Return a message beginning with SUCCESS or ERROR.
        """
        root = ywFile._tree.getroot()

        # Write locations to the xml element tree.

        for loc in root.iter('LOCATION'):
            lcId = loc.find('ID').text

            if lcId in ywFile.locations:

                if ywFile.locations[lcId].title is not None:
                    loc.find('Title').text = ywFile.locations[lcId].title

                if ywFile.locations[lcId].desc is not None:

                    if loc.find('Desc') is None:
                        ET.SubElement(
                            loc, 'Desc').text = ywFile.locations[lcId].desc

                    else:
                        loc.find('Desc').text = ywFile.locations[lcId].desc

                if ywFile.locations[lcId].aka is not None:

                    if loc.find('AKA') is None:
                        ET.SubElement(
                            loc, 'AKA').text = ywFile.locations[lcId].aka

                    else:
                        loc.find('AKA').text = ywFile.locations[lcId].aka

                if ywFile.locations[lcId].tags is not None:

                    if loc.find('Tags') is None:
                        ET.SubElement(loc, 'Tags').text = ';'.join(
                            ywFile.locations[lcId].tags)

                    else:
                        loc.find('Tags').text = ';'.join(
                            ywFile.locations[lcId].tags)

        # Write items to the xml element tree.

        for itm in root.iter('ITEM'):
            itId = itm.find('ID').text

            if itId in ywFile.items:

                if ywFile.items[itId].title is not None:
                    itm.find('Title').text = ywFile.items[itId].title

                if ywFile.items[itId].desc is not None:

                    if itm.find('Desc') is None:
                        ET.SubElement(
                            itm, 'Desc').text = ywFile.items[itId].desc

                    else:
                        itm.find('Desc').text = ywFile.items[itId].desc

                if ywFile.items[itId].aka is not None:

                    if itm.find('AKA') is None:
                        ET.SubElement(itm, 'AKA').text = ywFile.items[itId].aka

                    else:
                        itm.find('AKA').text = ywFile.items[itId].aka

                if ywFile.items[itId].tags is not None:

                    if itm.find('Tags') is None:
                        ET.SubElement(itm, 'Tags').text = ';'.join(
                            ywFile.items[itId].tags)

                    else:
                        itm.find('Tags').text = ';'.join(
                            ywFile.items[itId].tags)

        # Write characters to the xml element tree.

        for crt in root.iter('CHARACTER'):
            crId = crt.find('ID').text

            if crId in ywFile.characters:

                if ywFile.characters[crId].title is not None:
                    crt.find('Title').text = ywFile.characters[crId].title

                if ywFile.characters[crId].desc is not None:

                    if crt.find('Desc') is None:
                        ET.SubElement(
                            crt, 'Desc').text = ywFile.characters[crId].desc

                    else:
                        crt.find('Desc').text = ywFile.characters[crId].desc

                if ywFile.characters[crId].aka is not None:

                    if crt.find('AKA') is None:
                        ET.SubElement(
                            crt, 'AKA').text = ywFile.characters[crId].aka

                    else:
                        crt.find('AKA').text = ywFile.characters[crId].aka

                if ywFile.characters[crId].tags is not None:

                    if crt.find('Tags') is None:
                        ET.SubElement(crt, 'Tags').text = ';'.join(
                            ywFile.characters[crId].tags)

                    else:
                        crt.find('Tags').text = ';'.join(
                            ywFile.characters[crId].tags)

                if ywFile.characters[crId].notes is not None:

                    if crt.find('Notes') is None:
                        ET.SubElement(
                            crt, 'Notes').text = ywFile.characters[crId].notes

                    else:
                        crt.find(
                            'Notes').text = ywFile.characters[crId].notes

                if ywFile.characters[crId].bio is not None:

                    if crt.find('Bio') is None:
                        ET.SubElement(
                            crt, 'Bio').text = ywFile.characters[crId].bio

                    else:
                        crt.find('Bio').text = ywFile.characters[crId].bio

                if ywFile.characters[crId].goals is not None:

                    if crt.find('Goals') is None:
                        ET.SubElement(
                            crt, 'Goals').text = ywFile.characters[crId].goals

                    else:
                        crt.find(
                            'Goals').text = ywFile.characters[crId].goals

                if ywFile.characters[crId].fullName is not None:

                    if crt.find('FullName') is None:
                        ET.SubElement(
                            crt, 'FullName').text = ywFile.characters[crId].fullName

                    else:
                        crt.find(
                            'FullName').text = ywFile.characters[crId].fullName

                majorMarker = crt.find('Major')

                if majorMarker is not None:

                    if not ywFile.characters[crId].isMajor:
                        crt.remove(majorMarker)

                else:
                    if ywFile.characters[crId].isMajor:
                        ET.SubElement(crt, 'Major').text = '-1'

        # Write attributes at novel level to the xml element tree.

        prj = root.find('PROJECT')
        prj.find('Title').text = ywFile.title

        if ywFile.desc is not None:

            if prj.find('Desc') is None:
                ET.SubElement(prj, 'Desc').text = ywFile.desc

            else:
                prj.find('Desc').text = ywFile.desc

        if ywFile.author is not None:

            if prj.find('AuthorName') is None:
                ET.SubElement(prj, 'AuthorName').text = ywFile.author

            else:
                prj.find('AuthorName').text = ywFile.author

        prj.find('FieldTitle1').text = ywFile.fieldTitle1
        prj.find('FieldTitle2').text = ywFile.fieldTitle2
        prj.find('FieldTitle3').text = ywFile.fieldTitle3
        prj.find('FieldTitle4').text = ywFile.fieldTitle4

        # Write attributes at chapter level to the xml element tree.

        for chp in root.iter('CHAPTER'):
            chId = chp.find('ID').text

            if chId in ywFile.chapters:
                chp.find('Title').text = ywFile.chapters[chId].title

                if ywFile.chapters[chId].desc is not None:

                    if chp.find('Desc') is None:
                        ET.SubElement(
                            chp, 'Desc').text = ywFile.chapters[chId].desc

                    else:
                        chp.find('Desc').text = ywFile.chapters[chId].desc

                levelInfo = chp.find('SectionStart')

                if levelInfo is not None:

                    if ywFile.chapters[chId].chLevel == 0:
                        chp.remove(levelInfo)

                chp.find('Type').text = str(ywFile.chapters[chId].oldType)

                if ywFile.chapters[chId].chType is not None:

                    if chp.find('ChapterType') is not None:
                        chp.find('ChapterType').text = str(
                            ywFile.chapters[chId].chType)
                    else:
                        ET.SubElement(chp, 'ChapterType').text = str(
                            ywFile.chapters[chId].chType)

                if ywFile._VERSION == 5:

                    if ywFile.chapters[chId].oldType == 1:
                        ywFile.chapters[chId].isUnused = False

                if ywFile.chapters[chId].isUnused:

                    if chp.find('Unused') is None:
                        ET.SubElement(chp, 'Unused').text = '-1'

                elif chp.find('Unused') is not None:
                    chp.remove(chp.find('Unused'))

        # Write attributes at scene level to the xml element tree.

        for scn in root.iter('SCENE'):
            scId = scn.find('ID').text

            if scId in ywFile.scenes:

                if ywFile.scenes[scId].title is not None:
                    scn.find('Title').text = ywFile.scenes[scId].title

                if ywFile.scenes[scId].desc is not None:

                    if scn.find('Desc') is None:
                        ET.SubElement(
                            scn, 'Desc').text = ywFile.scenes[scId].desc

                    else:
                        scn.find('Desc').text = ywFile.scenes[scId].desc

                # Write scene content.

                if ywFile._VERSION > 5:

                    if ywFile.scenes[scId].sceneContent is not None:
                        scn.find(
                            'SceneContent').text = ywFile.scenes[scId].sceneContent
                        scn.find('WordCount').text = str(
                            ywFile.scenes[scId].wordCount)
                        scn.find('LetterCount').text = str(
                            ywFile.scenes[scId].letterCount)

                    try:
                        scn.remove(scn.find('RTFFile'))

                    except:
                        pass

                else:

                    try:
                        scn.remove(scn.find('SceneContent'))

                    except:
                        pass

                    if scn.find('RTFFile') is None:
                        ET.SubElement(scn, 'RTFFile')

                    try:
                        scn.find(
                            'RTFFile').text = ywFile.scenes[scId].rtfFile
                    except:
                        return 'ERROR: yWriter 5 RTF file not generated.'

                    scn.find('WordCount').text = str(
                        ywFile.scenes[scId].wordCount)
                    scn.find('LetterCount').text = str(
                        ywFile.scenes[scId].letterCount)

                if ywFile.scenes[scId].isUnused:

                    if scn.find('Unused') is None:
                        ET.SubElement(scn, 'Unused').text = '-1'

                elif scn.find('Unused') is not None:
                    scn.remove(scn.find('Unused'))

                if ywFile.scenes[scId].isNotesScene:

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

                if ywFile.scenes[scId].isTodoScene:

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

                if ywFile.scenes[scId].status is not None:
                    scn.find('Status').text = str(ywFile.scenes[scId].status)

                if ywFile.scenes[scId].sceneNotes is not None:

                    if scn.find('Notes') is None:
                        ET.SubElement(
                            scn, 'Notes').text = ywFile.scenes[scId].sceneNotes

                    else:
                        scn.find(
                            'Notes').text = ywFile.scenes[scId].sceneNotes

                if ywFile.scenes[scId].tags is not None:

                    if scn.find('Tags') is None:
                        ET.SubElement(scn, 'Tags').text = ';'.join(
                            ywFile.scenes[scId].tags)

                    else:
                        scn.find('Tags').text = ';'.join(
                            ywFile.scenes[scId].tags)

                if ywFile.scenes[scId].field1 is not None:

                    if scn.find('Field1') is None:
                        ET.SubElement(
                            scn, 'Field1').text = ywFile.scenes[scId].field1

                    else:
                        scn.find('Field1').text = ywFile.scenes[scId].field1

                if ywFile.scenes[scId].field2 is not None:

                    if scn.find('Field2') is None:
                        ET.SubElement(
                            scn, 'Field2').text = ywFile.scenes[scId].field2

                    else:
                        scn.find('Field2').text = ywFile.scenes[scId].field2

                if ywFile.scenes[scId].field3 is not None:

                    if scn.find('Field3') is None:
                        ET.SubElement(
                            scn, 'Field3').text = ywFile.scenes[scId].field3

                    else:
                        scn.find('Field3').text = ywFile.scenes[scId].field3

                if ywFile.scenes[scId].field4 is not None:

                    if scn.find('Field4') is None:
                        ET.SubElement(
                            scn, 'Field4').text = ywFile.scenes[scId].field4

                    else:
                        scn.find('Field4').text = ywFile.scenes[scId].field4

                if ywFile.scenes[scId].appendToPrev:

                    if scn.find('AppendToPrev') is None:
                        ET.SubElement(scn, 'AppendToPrev').text = '-1'

                elif scn.find('AppendToPrev') is not None:
                    scn.remove(scn.find('AppendToPrev'))

                # Date/time information

                if (ywFile.scenes[scId].date is not None) and (ywFile.scenes[scId].time is not None):
                    dateTime = ywFile.scenes[scId].date + \
                        ' ' + ywFile.scenes[scId].time

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

                elif (ywFile.scenes[scId].day is not None) or (ywFile.scenes[scId].hour is not None) or (ywFile.scenes[scId].minute is not None):

                    if scn.find('SpecificDateTime') is not None:
                        scn.remove(scn.find('SpecificDateTime'))

                    if scn.find('SpecificDateMode') is not None:
                        scn.remove(scn.find('SpecificDateMode'))

                    if ywFile.scenes[scId].day is not None:

                        if scn.find('Day') is not None:
                            scn.find('Day').text = ywFile.scenes[scId].day

                        else:
                            ET.SubElement(
                                scn, 'Day').text = ywFile.scenes[scId].day

                    if ywFile.scenes[scId].hour is not None:

                        if scn.find('Hour') is not None:
                            scn.find('Hour').text = ywFile.scenes[scId].hour

                        else:
                            ET.SubElement(
                                scn, 'Hour').text = ywFile.scenes[scId].hour

                    if ywFile.scenes[scId].minute is not None:

                        if scn.find('Minute') is not None:
                            scn.find(
                                'Minute').text = ywFile.scenes[scId].minute

                        else:
                            ET.SubElement(
                                scn, 'Minute').text = ywFile.scenes[scId].minute

                if ywFile.scenes[scId].lastsDays is not None:

                    if scn.find('LastsDays') is not None:
                        scn.find(
                            'LastsDays').text = ywFile.scenes[scId].lastsDays

                    else:
                        ET.SubElement(
                            scn, 'LastsDays').text = ywFile.scenes[scId].lastsDays

                if ywFile.scenes[scId].lastsHours is not None:

                    if scn.find('LastsHours') is not None:
                        scn.find(
                            'LastsHours').text = ywFile.scenes[scId].lastsHours

                    else:
                        ET.SubElement(
                            scn, 'LastsHours').text = ywFile.scenes[scId].lastsHours

                if ywFile.scenes[scId].lastsMinutes is not None:

                    if scn.find('LastsMinutes') is not None:
                        scn.find(
                            'LastsMinutes').text = ywFile.scenes[scId].lastsMinutes

                    else:
                        ET.SubElement(
                            scn, 'LastsMinutes').text = ywFile.scenes[scId].lastsMinutes

                # Plot related information

                if ywFile.scenes[scId].isReactionScene:

                    if scn.find('ReactionScene') is None:
                        ET.SubElement(scn, 'ReactionScene').text = '-1'

                elif scn.find('ReactionScene') is not None:
                    scn.remove(scn.find('ReactionScene'))

                if ywFile.scenes[scId].isSubPlot:

                    if scn.find('SubPlot') is None:
                        ET.SubElement(scn, 'SubPlot').text = '-1'

                elif scn.find('SubPlot') is not None:
                    scn.remove(scn.find('SubPlot'))

                if ywFile.scenes[scId].goal is not None:

                    if scn.find('Goal') is None:
                        ET.SubElement(
                            scn, 'Goal').text = ywFile.scenes[scId].goal

                    else:
                        scn.find('Goal').text = ywFile.scenes[scId].goal

                if ywFile.scenes[scId].conflict is not None:

                    if scn.find('Conflict') is None:
                        ET.SubElement(
                            scn, 'Conflict').text = ywFile.scenes[scId].conflict

                    else:
                        scn.find(
                            'Conflict').text = ywFile.scenes[scId].conflict

                if ywFile.scenes[scId].outcome is not None:

                    if scn.find('Outcome') is None:
                        ET.SubElement(
                            scn, 'Outcome').text = ywFile.scenes[scId].outcome

                    else:
                        scn.find(
                            'Outcome').text = ywFile.scenes[scId].outcome

                if ywFile.scenes[scId].characters is not None:
                    characters = scn.find('Characters')

                    for oldCrId in characters.findall('CharID'):
                        characters.remove(oldCrId)

                    for crId in ywFile.scenes[scId].characters:
                        ET.SubElement(characters, 'CharID').text = crId

                if ywFile.scenes[scId].locations is not None:
                    locations = scn.find('Locations')

                    for oldLcId in locations.findall('LocID'):
                        locations.remove(oldLcId)

                    for lcId in ywFile.scenes[scId].locations:
                        ET.SubElement(locations, 'LocID').text = lcId

                if ywFile.scenes[scId].items is not None:
                    items = scn.find('Items')

                    for oldItId in items.findall('ItemID'):
                        items.remove(oldItId)

                    for itId in ywFile.scenes[scId].items:
                        ET.SubElement(items, 'ItemID').text = itId
