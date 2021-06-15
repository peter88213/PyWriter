"""Provide a strategy class to build an yWriter 7 xml tree.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import xml.etree.ElementTree as ET


class Yw7TreeBuilder():
    """Build yWriter 7 project xml tree."""

    TAG = 'YWRITER7'
    VER = '7'

    def build_element_tree(self, ywProject):
        """Modify the yWriter project attributes of an existing xml element tree.
        Return a message beginning with SUCCESS or ERROR.
        """

        def create_scene_subtree(xmlScn, prjScn):
            ET.SubElement(xmlScn, 'ID').text = scId

            if prjScn.title is not None:
                ET.SubElement(xmlScn, 'Title').text = prjScn.title

            for chId in ywProject.chapters:

                if scId in ywProject.chapters[chId].srtScenes:
                    ET.SubElement(xmlScn, 'BelongsToChID').text = chId
                    break

            if prjScn.desc is not None:
                ET.SubElement(xmlScn, 'Desc').text = prjScn.desc

            if prjScn.sceneContent is not None:
                ET.SubElement(xmlScn,
                              'SceneContent').text = prjScn.sceneContent
                ET.SubElement(xmlScn, 'WordCount').text = str(prjScn.wordCount)
                ET.SubElement(xmlScn, 'LetterCount').text = str(
                    prjScn.letterCount)

            if prjScn.isUnused:
                ET.SubElement(xmlScn, 'Unused').text = '-1'

            scFields = ET.SubElement(xmlScn, 'Fields')

            if prjScn.isNotesScene:
                ET.SubElement(scFields, 'Field_SceneType').text = '1'

            elif prjScn.isTodoScene:
                ET.SubElement(scFields, 'Field_SceneType').text = '2'

            if prjScn.status is not None:
                ET.SubElement(xmlScn, 'Status').text = str(prjScn.status)

            if prjScn.sceneNotes is not None:
                ET.SubElement(xmlScn, 'Notes').text = prjScn.sceneNotes

            if prjScn.tags is not None:
                ET.SubElement(xmlScn, 'Tags').text = ';'.join(prjScn.tags)

            if prjScn.field1 is not None:
                ET.SubElement(xmlScn, 'Field1').text = prjScn.field1

            if prjScn.field2 is not None:
                ET.SubElement(xmlScn, 'Field2').text = prjScn.field2

            if prjScn.field3 is not None:
                ET.SubElement(xmlScn, 'Field3').text = prjScn.field3

            if prjScn.field4 is not None:
                ET.SubElement(xmlScn, 'Field4').text = prjScn.field4

            if prjScn.appendToPrev:
                ET.SubElement(xmlScn, 'AppendToPrev').text = '-1'

            # Date/time information

            if (prjScn.date is not None) and (prjScn.time is not None):
                dateTime = ' '.join(prjScn.date, prjScn.time)
                ET.SubElement(xmlScn, 'SpecificDateTime').text = dateTime
                ET.SubElement(xmlScn, 'SpecificDateMode').text = '-1'

            elif (prjScn.day is not None) or (prjScn.hour is not None) or (prjScn.minute is not None):

                if prjScn.day is not None:
                    ET.SubElement(xmlScn, 'Day').text = prjScn.day

                if prjScn.hour is not None:
                    ET.SubElement(xmlScn, 'Hour').text = prjScn.hour

                if prjScn.minute is not None:
                    ET.SubElement(xmlScn, 'Minute').text = prjScn.minute

            if prjScn.lastsDays is not None:
                ET.SubElement(xmlScn, 'LastsDays').text = prjScn.lastsDays

            if prjScn.lastsHours is not None:
                ET.SubElement(xmlScn, 'LastsHours').text = prjScn.lastsHours

            if prjScn.lastsMinutes is not None:
                ET.SubElement(
                    xmlScn, 'LastsMinutes').text = prjScn.lastsMinutes

            # Plot related information

            if prjScn.isReactionScene:
                ET.SubElement(xmlScn, 'ReactionScene').text = '-1'

            if prjScn.isSubPlot:
                ET.SubElement(xmlScn, 'SubPlot').text = '-1'

            if prjScn.goal is not None:
                ET.SubElement(xmlScn, 'Goal').text = prjScn.goal

            if prjScn.conflict is not None:
                ET.SubElement(xmlScn, 'Conflict').text = prjScn.conflict

            if prjScn.outcome is not None:
                ET.SubElement(xmlScn, 'Outcome').text = prjScn.outcome

            if prjScn.characters is not None:
                scCharacters = ET.SubElement(xmlScn, 'Characters')

                for crId in prjScn.characters:
                    ET.SubElement(scCharacters, 'CharID').text = crId

            if prjScn.locations is not None:
                scLocations = ET.SubElement(xmlScn, 'Locations')

                for lcId in prjScn.locations:
                    ET.SubElement(scLocations, 'LocID').text = lcId

            if prjScn.items is not None:
                scItems = ET.SubElement(xmlScn, 'Items')

                for itId in prjScn.items:
                    ET.SubElement(scItems, 'ItemID').text = itId

        def build_scene_subtree(xmlScn, prjScn):

            if prjScn.title is not None:

                try:
                    xmlScn.find('Title').text = prjScn.title

                except(AttributeError):
                    ET.SubElement(xmlScn, 'Title').text = prjScn.title

            if prjScn.desc is not None:

                try:
                    xmlScn.find('Desc').text = prjScn.desc

                except(AttributeError):
                    ET.SubElement(xmlScn, 'Desc').text = prjScn.desc

            # Scene content is written in subclasses.

            if prjScn.isUnused:

                if xmlScn.find('Unused') is None:
                    ET.SubElement(xmlScn, 'Unused').text = '-1'

            elif xmlScn.find('Unused') is not None:
                xmlScn.remove(xmlScn.find('Unused'))

            if prjScn.isNotesScene:

                try:
                    scFields = xmlScn.find('Fields')

                except(AttributeError):
                    scFields = ET.SubElement(xmlScn, 'Fields')

                if scFields.find('Field_SceneType') is None:
                    ET.SubElement(scFields, 'Field_SceneType').text = '1'

            elif xmlScn.find('Fields') is not None:
                scFields = xmlScn.find('Fields')

                if scFields.find('Field_SceneType') is not None:

                    if scFields.find('Field_SceneType').text == '1':
                        scFields.remove(scFields.find('Field_SceneType'))

            if prjScn.isTodoScene:

                try:
                    scFields = xmlScn.find('Fields')

                except(AttributeError):
                    scFields = ET.SubElement(xmlScn, 'Fields')

                if scFields.find('Field_SceneType') is None:
                    ET.SubElement(scFields, 'Field_SceneType').text = '2'

            elif xmlScn.find('Fields') is not None:
                scFields = xmlScn.find('Fields')

                if scFields.find('Field_SceneType') is not None:

                    if scFields.find('Field_SceneType').text == '2':
                        scFields.remove(scFields.find('Field_SceneType'))

            if prjScn.status is not None:
                xmlScn.find('Status').text = str(prjScn.status)

            if prjScn.sceneNotes is not None:

                try:
                    xmlScn.find('Notes').text = prjScn.sceneNotes

                except(AttributeError):
                    ET.SubElement(xmlScn, 'Notes').text = prjScn.sceneNotes

            if prjScn.tags is not None:

                try:
                    xmlScn.find('Tags').text = ';'.join(prjScn.tags)

                except(AttributeError):
                    ET.SubElement(xmlScn, 'Tags').text = ';'.join(prjScn.tags)

            if prjScn.field1 is not None:

                try:
                    xmlScn.find('Field1').text = prjScn.field1

                except(AttributeError):
                    ET.SubElement(xmlScn, 'Field1').text = prjScn.field1

            if prjScn.field2 is not None:

                try:
                    xmlScn.find('Field2').text = prjScn.field2

                except(AttributeError):
                    ET.SubElement(xmlScn, 'Field2').text = prjScn.field2

            if prjScn.field3 is not None:

                try:
                    xmlScn.find('Field3').text = prjScn.field3

                except(AttributeError):
                    ET.SubElement(xmlScn, 'Field3').text = prjScn.field3

            if prjScn.field4 is not None:

                try:
                    xmlScn.find('Field4').text = prjScn.field4

                except(AttributeError):
                    ET.SubElement(xmlScn, 'Field4').text = prjScn.field4

            if prjScn.appendToPrev:

                if xmlScn.find('AppendToPrev') is None:
                    ET.SubElement(xmlScn, 'AppendToPrev').text = '-1'

            elif xmlScn.find('AppendToPrev') is not None:
                xmlScn.remove(xmlScn.find('AppendToPrev'))

            # Date/time information

            if (prjScn.date is not None) and (prjScn.time is not None):
                dateTime = prjScn.date + ' ' + prjScn.time

                if xmlScn.find('SpecificDateTime') is not None:
                    xmlScn.find('SpecificDateTime').text = dateTime

                else:
                    ET.SubElement(xmlScn, 'SpecificDateTime').text = dateTime
                    ET.SubElement(xmlScn, 'SpecificDateMode').text = '-1'

                    if xmlScn.find('Day') is not None:
                        xmlScn.remove(xmlScn.find('Day'))

                    if xmlScn.find('Hour') is not None:
                        xmlScn.remove(xmlScn.find('Hour'))

                    if xmlScn.find('Minute') is not None:
                        xmlScn.remove(xmlScn.find('Minute'))

            elif (prjScn.day is not None) or (prjScn.hour is not None) or (prjScn.minute is not None):

                if xmlScn.find('SpecificDateTime') is not None:
                    xmlScn.remove(xmlScn.find('SpecificDateTime'))

                if xmlScn.find('SpecificDateMode') is not None:
                    xmlScn.remove(xmlScn.find('SpecificDateMode'))

                if prjScn.day is not None:

                    try:
                        xmlScn.find('Day').text = prjScn.day

                    except(AttributeError):
                        ET.SubElement(xmlScn, 'Day').text = prjScn.day

                if prjScn.hour is not None:

                    try:
                        xmlScn.find('Hour').text = prjScn.hour

                    except(AttributeError):
                        ET.SubElement(xmlScn, 'Hour').text = prjScn.hour

                if prjScn.minute is not None:

                    try:
                        xmlScn.find('Minute').text = prjScn.minute

                    except(AttributeError):
                        ET.SubElement(xmlScn, 'Minute').text = prjScn.minute

            if prjScn.lastsDays is not None:

                try:
                    xmlScn.find('LastsDays').text = prjScn.lastsDays

                except(AttributeError):
                    ET.SubElement(xmlScn, 'LastsDays').text = prjScn.lastsDays

            if prjScn.lastsHours is not None:

                try:
                    xmlScn.find('LastsHours').text = prjScn.lastsHours

                except(AttributeError):
                    ET.SubElement(
                        xmlScn, 'LastsHours').text = prjScn.lastsHours

            if prjScn.lastsMinutes is not None:

                try:
                    xmlScn.find('LastsMinutes').text = prjScn.lastsMinutes

                except(AttributeError):
                    ET.SubElement(
                        xmlScn, 'LastsMinutes').text = prjScn.lastsMinutes

            # Plot related information

            if prjScn.isReactionScene:

                if xmlScn.find('ReactionScene') is None:
                    ET.SubElement(xmlScn, 'ReactionScene').text = '-1'

            elif xmlScn.find('ReactionScene') is not None:
                xmlScn.remove(xmlScn.find('ReactionScene'))

            if prjScn.isSubPlot:

                if xmlScn.find('SubPlot') is None:
                    ET.SubElement(xmlScn, 'SubPlot').text = '-1'

            elif xmlScn.find('SubPlot') is not None:
                xmlScn.remove(xmlScn.find('SubPlot'))

            if prjScn.goal is not None:

                try:
                    xmlScn.find('Goal').text = prjScn.goal

                except(AttributeError):
                    ET.SubElement(xmlScn, 'Goal').text = prjScn.goal

            if prjScn.conflict is not None:

                try:
                    xmlScn.find('Conflict').text = prjScn.conflict

                except(AttributeError):
                    ET.SubElement(xmlScn, 'Conflict').text = prjScn.conflict

            if prjScn.outcome is not None:

                try:
                    xmlScn.find('Outcome').text = prjScn.outcome

                except(AttributeError):
                    ET.SubElement(xmlScn, 'Outcome').text = prjScn.outcome

            if prjScn.characters is not None:
                characters = xmlScn.find('Characters')

                for oldCrId in characters.findall('CharID'):
                    characters.remove(oldCrId)

                for crId in prjScn.characters:
                    ET.SubElement(characters, 'CharID').text = crId

            if prjScn.locations is not None:
                locations = xmlScn.find('Locations')

                for oldLcId in locations.findall('LocID'):
                    locations.remove(oldLcId)

                for lcId in prjScn.locations:
                    ET.SubElement(locations, 'LocID').text = lcId

            if prjScn.items is not None:
                items = xmlScn.find('Items')

                for oldItId in items.findall('ItemID'):
                    items.remove(oldItId)

                for itId in prjScn.items:
                    ET.SubElement(items, 'ItemID').text = itId

        def create_chapter_subtree(xmlChp, prjChp, sortOrder):
            ET.SubElement(xmlChp, 'ID').text = chId
            ET.SubElement(xmlChp, 'SortOrder').text = str(sortOrder)

            if prjChp.title is not None:
                ET.SubElement(xmlChp, 'Title').text = prjChp.title

            if prjChp.desc is not None:
                ET.SubElement(xmlChp, 'Desc').text = prjChp.desc

            if prjChp.chLevel == 1:
                ET.SubElement(xmlChp, 'SectionStart').text = '-1'

            if prjChp.oldType is not None:
                ET.SubElement(xmlChp, 'Type').text = str(prjChp.oldType)

            if prjChp.chType is not None:
                ET.SubElement(xmlChp, 'ChapterType').text = str(prjChp.chType)

            if prjChp.isUnused:
                ET.SubElement(xmlChp, 'Unused').text = '-1'

            sortSc = ET.SubElement(xmlChp, 'Scenes')

            for scId in prjChp.srtScenes:
                ET.SubElement(sortSc, 'ScID').text = scId

            chFields = ET.SubElement(xmlChp, 'Fields')

            if prjChp.title is not None:

                if prjChp.title.startswith('@'):
                    prjChp.suppressChapterTitle = True

            if prjChp.suppressChapterTitle:
                ET.SubElement(
                    chFields, 'Field_SuppressChapterTitle').text = '1'

        def build_chapter_subtree(xmlChp, prjChp, sortOrder):

            try:
                xmlChp.find('SortOrder').text = str(sortOrder)

            except(AttributeError):
                ET.SubElement(xmlChp, 'SortOrder').text = str(sortOrder)

            try:
                xmlChp.find('Title').text = prjChp.title

            except(AttributeError):
                ET.SubElement(xmlChp, 'Title').text = prjChp.title

            if prjChp.desc is not None:

                try:
                    xmlChp.find('Desc').text = prjChp.desc

                except(AttributeError):
                    ET.SubElement(xmlChp, 'Desc').text = prjChp.desc

            if xmlChp.find('SectionStart') is not None:

                if prjChp.chLevel == 0:
                    xmlChp.remove(xmlChp.find('SectionStart'))

            elif prjChp.chLevel == 1:
                ET.SubElement(xmlChp, 'SectionStart').text = '-1'

            if prjChp.oldType is not None:

                try:
                    xmlChp.find('Type').text = str(prjChp.oldType)

                except(AttributeError):
                    ET.SubElement(xmlChp, 'Type').text = str(prjChp.oldType)

            if prjChp.chType is not None:

                try:
                    xmlChp.find('ChapterType').text = str(prjChp.chType)

                except(AttributeError):
                    ET.SubElement(xmlChp, 'ChapterType').text = str(
                        prjChp.chType)

            if prjChp.isUnused:

                if xmlChp.find('Unused') is None:
                    ET.SubElement(xmlChp, 'Unused').text = '-1'

            elif xmlChp.find('Unused') is not None:
                xmlChp.remove(xmlChp.find('Unused'))

        def create_location_subtree(xmlLoc, prjLoc, sortOrder):
            ET.SubElement(xmlLoc, 'ID').text = lcId

            if prjLoc.title is not None:
                ET.SubElement(xmlLoc, 'Title').text = prjLoc.title

            if prjLoc.image is not None:
                ET.SubElement(xmlLoc, 'ImageFile').text = prjLoc.image

            if prjLoc.desc is not None:
                ET.SubElement(xmlLoc, 'Desc').text = prjLoc.desc

            if prjLoc.aka is not None:
                ET.SubElement(xmlLoc, 'AKA').text = prjLoc.aka

            if prjLoc.tags is not None:
                ET.SubElement(xmlLoc, 'Tags').text = ';'.join(prjLoc.tags)

            ET.SubElement(xmlLoc, 'SortOrder').text = str(sortOrder)

        def create_item_subtree(xmlItm, prjItm, sortOrder):
            ET.SubElement(xmlItm, 'ID').text = itId

            if prjItm.title is not None:
                ET.SubElement(xmlItm, 'Title').text = prjItm.title

            if prjItm.image is not None:
                ET.SubElement(xmlItm, 'ImageFile').text = prjItm.image

            if prjItm.desc is not None:
                ET.SubElement(xmlItm, 'Desc').text = prjItm.desc

            if prjItm.aka is not None:
                ET.SubElement(xmlItm, 'AKA').text = prjItm.aka

            if prjItm.tags is not None:
                ET.SubElement(xmlItm, 'Tags').text = ';'.join(prjItm.tags)

            ET.SubElement(xmlItm, 'SortOrder').text = str(sortOrder)

        def create_character_subtree(xmlCrt, prjCrt, sortOrder):
            ET.SubElement(xmlCrt, 'ID').text = crId

            if prjCrt.title is not None:
                ET.SubElement(xmlCrt, 'Title').text = prjCrt.title

            if prjCrt.desc is not None:
                ET.SubElement(xmlCrt, 'Desc').text = prjCrt.desc

            if prjCrt.image is not None:
                ET.SubElement(xmlCrt, 'ImageFile').text = prjCrt.image

            ET.SubElement(xmlCrt, 'SortOrder').text = str(sortOrder)

            if prjCrt.notes is not None:
                ET.SubElement(xmlCrt, 'Notes').text = prjCrt.notes

            if prjCrt.aka is not None:
                ET.SubElement(xmlCrt, 'AKA').text = prjCrt.aka

            if prjCrt.tags is not None:
                ET.SubElement(xmlCrt, 'Tags').text = ';'.join(
                    prjCrt.tags)

            if prjCrt.bio is not None:
                ET.SubElement(xmlCrt, 'Bio').text = prjCrt.bio

            if prjCrt.goals is not None:
                ET.SubElement(xmlCrt, 'Goals').text = prjCrt.goals

            if prjCrt.fullName is not None:
                ET.SubElement(xmlCrt, 'FullName').text = prjCrt.fullName

            if prjCrt.isMajor:
                ET.SubElement(xmlCrt, 'Major').text = '-1'

        def build_project_subtree(xmlPrj, ywProject):

            try:
                xmlPrj.find('Ver').text = self.VER

            except(AttributeError):
                ET.SubElement(xmlPrj, 'Ver').text = self.VER

            if ywProject.title is not None:

                try:
                    xmlPrj.find('Title').text = ywProject.title

                except(AttributeError):
                    ET.SubElement(xmlPrj, 'Title').text = ywProject.title

            if ywProject.desc is not None:

                try:
                    xmlPrj.find('Desc').text = ywProject.desc

                except(AttributeError):
                    ET.SubElement(xmlPrj, 'Desc').text = ywProject.desc

            if ywProject.author is not None:

                try:
                    xmlPrj.find('AuthorName').text = ywProject.author

                except(AttributeError):
                    ET.SubElement(xmlPrj, 'AuthorName').text = ywProject.author

            if ywProject.fieldTitle1 is not None:

                try:
                    xmlPrj.find('FieldTitle1').text = ywProject.fieldTitle1

                except(AttributeError):
                    ET.SubElement(
                        xmlPrj, 'FieldTitle1').text = ywProject.fieldTitle1

            if ywProject.fieldTitle2 is not None:

                try:
                    xmlPrj.find('FieldTitle2').text = ywProject.fieldTitle2

                except(AttributeError):
                    ET.SubElement(
                        xmlPrj, 'FieldTitle2').text = ywProject.fieldTitle2

            if ywProject.fieldTitle3 is not None:

                try:
                    xmlPrj.find('FieldTitle3').text = ywProject.fieldTitle3

                except(AttributeError):
                    ET.SubElement(
                        xmlPrj, 'FieldTitle3').text = ywProject.fieldTitle3

            if ywProject.fieldTitle4 is not None:

                try:
                    xmlPrj.find('FieldTitle4').text = ywProject.fieldTitle4

                except(AttributeError):
                    ET.SubElement(
                        xmlPrj, 'FieldTitle4').text = ywProject.fieldTitle4

        xmlScenes = {}
        xmlChapters = {}

        try:
            root = ywProject.tree.getroot()
            xmlPrj = root.find('PROJECT')
            locations = root.find('LOCATIONS')
            items = root.find('ITEMS')
            characters = root.find('CHARACTERS')
            scenes = root.find('SCENES')
            chapters = root.find('CHAPTERS')

        except(AttributeError):
            root = ET.Element(self.TAG)
            xmlPrj = ET.SubElement(root, 'PROJECT')
            locations = ET.SubElement(root, 'LOCATIONS')
            items = ET.SubElement(root, 'ITEMS')
            characters = ET.SubElement(root, 'CHARACTERS')
            scenes = ET.SubElement(root, 'SCENES')
            chapters = ET.SubElement(root, 'CHAPTERS')

        #--- Process project attributes.

        build_project_subtree(xmlPrj, ywProject)

        #--- Process locations.
        # Remove LOCATION entries in order to rewrite
        # the LOCATIONS section in a modified sort order.

        for xmlLoc in locations.findall('LOCATION'):
            locations.remove(xmlLoc)

        # Add the new XML location subtrees to the project tree.

        sortOrder = 0

        for lcId in ywProject.srtLocations:
            sortOrder += 1
            xmlLoc = ET.SubElement(locations, 'LOCATION')
            create_location_subtree(
                xmlLoc, ywProject.locations[lcId], sortOrder)

        #--- Process items.
        # Remove ITEM entries in order to rewrite
        # the ITEMS section in a modified sort order.

        for xmlItm in items.findall('ITEM'):
            items.remove(xmlItm)

        # Add the new XML item subtrees to the project tree.

        sortOrder = 0

        for itId in ywProject.srtItems:
            sortOrder += 1
            xmlItm = ET.SubElement(items, 'ITEM')
            create_item_subtree(xmlItm, ywProject.items[itId], sortOrder)

        #--- Process characters.
        # Remove CHARACTER entries in order to rewrite
        # the CHARACTERS section in a modified sort order.

        for xmlCrt in characters.findall('CHARACTER'):
            characters.remove(xmlCrt)

        # Add the new XML character subtrees to the project tree.

        sortOrder = 0

        for crId in ywProject.srtCharacters:
            sortOrder += 1
            xmlCrt = ET.SubElement(characters, 'CHARACTER')
            create_character_subtree(
                xmlCrt, ywProject.characters[crId], sortOrder)

        #--- Process scenes.
        # Save the original XML scene subtrees
        # and remove them from the project tree.

        for xmlScn in scenes.findall('SCENE'):
            scId = xmlScn.find('ID').text
            xmlScenes[scId] = xmlScn
            scenes.remove(xmlScn)

        # Add the new XML scene subtrees to the project tree.

        for scId in ywProject.scenes:

            if scId in xmlScenes:
                build_scene_subtree(xmlScenes[scId], ywProject.scenes[scId])

            else:
                xmlScenes[scId] = ET.Element('SCENE')
                create_scene_subtree(xmlScenes[scId], ywProject.scenes[scId])

            scenes.append(xmlScenes[scId])

        #--- Process chapters.
        # Save the original XML chapter subtree
        # and remove it from the project tree.

        for xmlChp in chapters.findall('CHAPTER'):
            chId = xmlChp.find('ID').text
            xmlChapters[chId] = xmlChp
            chapters.remove(xmlChp)

        # Add the new XML chapter subtrees to the project tree.

        sortOrder = 0

        for chId in ywProject.chapters:
            sortOrder += 1

            if chId in xmlChapters:
                build_chapter_subtree(
                    xmlChapters[chId], ywProject.chapters[chId], sortOrder)

            else:
                xmlChapters[chId] = ET.Element('CHAPTER')
                # ET.SubElement(xmlChapters[chId], 'ID').text = chId

                # build_chapter_subtree(
                create_chapter_subtree(
                    xmlChapters[chId], ywProject.chapters[chId], sortOrder)

            chapters.append(xmlChapters[chId])

        self.indent_xml(root)
        ywProject.tree = ET.ElementTree(root)

        # Write version-dependent scene contents to the xml element tree.

        return self.put_scene_contents(ywProject)

    def put_scene_contents(self, ywProject):
        """Modify the scene contents of an existing xml element tree.
        Return a message beginning with SUCCESS or ERROR.
        Strategy method for the yw7 file format variant.
        """

        root = ywProject.tree.getroot()

        for scn in root.iter('SCENE'):
            scId = scn.find('ID').text

            if ywProject.scenes[scId].sceneContent is not None:
                scn.find(
                    'SceneContent').text = ywProject.scenes[scId].sceneContent
                scn.find('WordCount').text = str(
                    ywProject.scenes[scId].wordCount)
                scn.find('LetterCount').text = str(
                    ywProject.scenes[scId].letterCount)

            try:
                scn.remove(scn.find('RTFFile'))

            except:
                pass

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
