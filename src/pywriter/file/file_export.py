"""FileExport - Generic template-based file exporter.

* Merge a novel object's attributes.
* Convert yw7 markup to target format. 
* Create a template-based output file.
* This class is generic and contains no conversion algorithm and no templates.

Part of the PyWriter project.
Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
from string import Template

from pywriter.model.character import Character
from pywriter.model.scene import Scene
from pywriter.model.novel import Novel


class FileExport(Novel):
    """Abstract yWriter project file exporter representation.
    To be overwritten by subclasses providing file type specific 
    markup converters and templates.
    """

    fileHeader = ''
    partTemplate = ''
    chapterTemplate = ''
    notesChapterTemplate = ''
    todoChapterTemplate = ''
    unusedChapterTemplate = ''
    notExportedChapterTemplate = ''
    sceneTemplate = ''
    appendedSceneTemplate = ''
    notesSceneTemplate = ''
    todoSceneTemplate = ''
    unusedSceneTemplate = ''
    notExportedSceneTemplate = ''
    sceneDivider = ''
    chapterEndTemplate = ''
    unusedChapterEndTemplate = ''
    notExportedChapterEndTemplate = ''
    notesChapterEndTemplate = ''
    characterTemplate = ''
    locationTemplate = ''
    itemTemplate = ''
    fileFooter = ''

    def convert_from_yw(self, text):
        """Convert yw7 markup to target format.
        To be overwritten by file format specific subclasses.
        """

        if text is None:
            text = ''

        return(text)

    def merge(self, novel):
        """Copy required attributes of the novel object.
        Return a message beginning with SUCCESS or ERROR.
        """

        if novel.title is not None:
            self.title = novel.title

        else:
            self.title = ''

        if novel.desc is not None:
            self.desc = novel.desc

        else:
            self.desc = ''

        if novel.author is not None:
            self.author = novel.author

        else:
            self.author = ''

        if novel.fieldTitle1 is not None:
            self.fieldTitle1 = novel.fieldTitle1

        else:
            self.fieldTitle1 = 'Field 1'

        if novel.fieldTitle2 is not None:
            self.fieldTitle2 = novel.fieldTitle2

        else:
            self.fieldTitle2 = 'Field 2'

        if novel.fieldTitle3 is not None:
            self.fieldTitle3 = novel.fieldTitle3

        else:
            self.fieldTitle3 = 'Field 3'

        if novel.fieldTitle4 is not None:
            self.fieldTitle4 = novel.fieldTitle4

        else:
            self.fieldTitle4 = 'Field 4'

        if novel.srtChapters != []:
            self.srtChapters = novel.srtChapters

        if novel.scenes is not None:
            self.scenes = novel.scenes

        if novel.chapters is not None:
            self.chapters = novel.chapters

        if novel.srtCharacters != []:
            self.srtCharacters = novel.srtCharacters
            self.characters = novel.characters

        if novel.srtLocations != []:
            self.srtLocations = novel.srtLocations
            self.locations = novel.locations

        if novel.srtItems != []:
            self.srtItems = novel.srtItems
            self.items = novel.items

        return 'SUCCESS'

    def get_fileHeaderMapping(self):
        """Return a mapping dictionary for the project section. 
        """
        projectTemplateMapping = dict(
            Title=self.title,
            Desc=self.convert_from_yw(self.desc),
            AuthorName=self.author,
            FieldTitle1=self.fieldTitle1,
            FieldTitle2=self.fieldTitle2,
            FieldTitle3=self.fieldTitle3,
            FieldTitle4=self.fieldTitle4,
        )

        for key in projectTemplateMapping:
            if projectTemplateMapping[key] is None:
                projectTemplateMapping[key] = ''

        return projectTemplateMapping

    def get_chapterMapping(self, chId, chapterNumber):
        """Return a mapping dictionary for a chapter section. 
        """
        chapterMapping = dict(
            ID=chId,
            ChapterNumber=chapterNumber,
            Title=self.chapters[chId].get_title(),
            Desc=self.convert_from_yw(self.chapters[chId].desc),
            ProjectName=self.projectName,
            ProjectPath=self.projectPath,
        )

        for key in chapterMapping:
            if chapterMapping[key] is None:
                chapterMapping[key] = ''

        return chapterMapping

    def get_sceneMapping(self, scId, sceneNumber, wordsTotal, lettersTotal):
        """Return a mapping dictionary for a scene section. 
        """

        if self.scenes[scId].tags is not None:
            tags = ', '.join(self.scenes[scId].tags)

        else:
            tags = ''

        try:
            # Note: Due to a bug, yWriter scenes might hold invalid
            # viepoint characters
            sChList = []

            for chId in self.scenes[scId].characters:
                sChList.append(self.characters[chId].title)

            sceneChars = ', '.join(sChList)
            viewpointChar = sChList[0]

        except:
            sceneChars = ''
            viewpointChar = ''

        if self.scenes[scId].locations is not None:
            sLcList = []

            for lcId in self.scenes[scId].locations:
                sLcList.append(self.locations[lcId].title)

            sceneLocs = ', '.join(sLcList)

        else:
            sceneLocs = ''

        if self.scenes[scId].items is not None:
            sItList = []

            for itId in self.scenes[scId].items:
                sItList.append(self.items[itId].title)

            sceneItems = ', '.join(sItList)

        else:
            sceneItems = ''

        if self.scenes[scId].isReactionScene:
            reactionScene = Scene.REACTION_MARKER

        else:
            reactionScene = Scene.ACTION_MARKER

        sceneMapping = dict(
            ID=scId,
            SceneNumber=sceneNumber,
            Title=self.scenes[scId].title,
            Desc=self.convert_from_yw(self.scenes[scId].desc),
            WordCount=str(self.scenes[scId].wordCount),
            WordsTotal=wordsTotal,
            LetterCount=str(self.scenes[scId].letterCount),
            LettersTotal=lettersTotal,
            Status=Scene.STATUS[self.scenes[scId].status],
            SceneContent=self.convert_from_yw(
                self.scenes[scId].sceneContent),
            FieldTitle1=self.fieldTitle1,
            FieldTitle2=self.fieldTitle2,
            FieldTitle3=self.fieldTitle3,
            FieldTitle4=self.fieldTitle4,
            Field1=self.scenes[scId].field1,
            Field2=self.scenes[scId].field2,
            Field3=self.scenes[scId].field3,
            Field4=self.scenes[scId].field4,
            Date=self.scenes[scId].date,
            Time=self.scenes[scId].time,
            Day=self.scenes[scId].day,
            Hour=self.scenes[scId].hour,
            Minute=self.scenes[scId].minute,
            LastsDays=self.scenes[scId].lastsDays,
            LastsHours=self.scenes[scId].lastsHours,
            LastsMinutes=self.scenes[scId].lastsMinutes,
            ReactionScene=reactionScene,
            Goal=self.convert_from_yw(self.scenes[scId].goal),
            Conflict=self.convert_from_yw(self.scenes[scId].conflict),
            Outcome=self.convert_from_yw(self.scenes[scId].outcome),
            Tags=tags,
            Characters=sceneChars,
            Viewpoint=viewpointChar,
            Locations=sceneLocs,
            Items=sceneItems,
            Notes=self.convert_from_yw(self.scenes[scId].sceneNotes),
            ProjectName=self.projectName,
            ProjectPath=self.projectPath,
        )

        for key in sceneMapping:
            if sceneMapping[key] is None:
                sceneMapping[key] = ''

        return sceneMapping

    def get_characterMapping(self, crId):
        """Return a mapping dictionary for a character section. 
        """

        if self.characters[crId].tags is not None:
            tags = ', '.join(self.characters[crId].tags)

        else:
            tags = ''

        if self.characters[crId].isMajor:
            characterStatus = Character.MAJOR_MARKER

        else:
            characterStatus = Character.MINOR_MARKER

        characterMapping = dict(
            ID=crId,
            Title=self.characters[crId].title,
            Desc=self.convert_from_yw(self.characters[crId].desc),
            Tags=tags,
            AKA=FileExport.convert_from_yw(self, self.characters[crId].aka),
            Notes=self.convert_from_yw(self.characters[crId].notes),
            Bio=self.convert_from_yw(self.characters[crId].bio),
            Goals=self.convert_from_yw(self.characters[crId].goals),
            FullName=FileExport.convert_from_yw(
                self, self.characters[crId].fullName),
            Status=characterStatus,
        )

        for key in characterMapping:
            if characterMapping[key] is None:
                characterMapping[key] = ''

        return characterMapping

    def get_locationMapping(self, lcId):
        """Return a mapping dictionary for a location section. 
        """

        if self.locations[lcId].tags is not None:
            tags = ', '.join(self.locations[lcId].tags)

        else:
            tags = ''

        locationMapping = dict(
            ID=lcId,
            Title=self.locations[lcId].title,
            Desc=self.convert_from_yw(self.locations[lcId].desc),
            Tags=tags,
            AKA=FileExport.convert_from_yw(self, self.locations[lcId].aka),
        )

        for key in locationMapping:
            if locationMapping[key] is None:
                locationMapping[key] = ''

        return locationMapping

    def get_itemMapping(self, itId):
        """Return a mapping dictionary for an item section. 
        """

        if self.items[itId].tags is not None:
            tags = ', '.join(self.items[itId].tags)

        else:
            tags = ''

        itemMapping = dict(
            ID=itId,
            Title=self.items[itId].title,
            Desc=self.convert_from_yw(self.items[itId].desc),
            Tags=tags,
            AKA=FileExport.convert_from_yw(self, self.items[itId].aka),
        )

        for key in itemMapping:
            if itemMapping[key] is None:
                itemMapping[key] = ''

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

            titles = '\n'.join(titlelist)

        except:
            titles = ''

        tagMapping = dict(
            Tag=tag,
            Elements=titles,
        )

        for key in tagMapping:
            if tagMapping[key] is None:
                tagMapping[key] = ''

        return tagMapping

    def get_fileHeader(self):
        """Process the file header.
        Return a list of strings.
        """
        lines = []

        template = Template(self.fileHeader)
        lines.append(template.safe_substitute(
            self.get_fileHeaderMapping()))

        return lines

    def get_scenes(self, chId, sceneNumber, wordsTotal, lettersTotal, doNotExport):
        """Process the scenes.
        Return a list of strings.
        """

        lines = []
        firstSceneInChapter = True

        for scId in self.chapters[chId].srtScenes:
            wordsTotal += self.scenes[scId].wordCount
            lettersTotal += self.scenes[scId].letterCount

            # The order counts; be aware that "Todo" and "Notes" scenes are
            # always unused.

            if self.scenes[scId].isTodoScene:

                if self.todoSceneTemplate != '':
                    template = Template(self.todoSceneTemplate)

                else:
                    continue

            elif self.scenes[scId].isNotesScene or self.chapters[chId].oldType == 1:
                # Scene is "Notes" (new file format) or "Info" (old file
                # format) scene.

                if self.notesSceneTemplate != '':
                    template = Template(self.notesSceneTemplate)

                else:
                    continue

            elif self.scenes[scId].isUnused or self.chapters[chId].isUnused:

                if self.unusedSceneTemplate != '':
                    template = Template(self.unusedSceneTemplate)

                else:
                    continue

            elif self.scenes[scId].doNotExport or doNotExport:

                if self.notExportedSceneTemplate != '':
                    template = Template(self.notExportedSceneTemplate)

                else:
                    continue

            else:
                sceneNumber += 1

                template = Template(self.sceneTemplate)

                if not firstSceneInChapter and self.scenes[scId].appendToPrev and self.appendedSceneTemplate != '':
                    template = Template(self.appendedSceneTemplate)

            if not (firstSceneInChapter or self.scenes[scId].appendToPrev):
                lines.append(self.sceneDivider)

            lines.append(template.safe_substitute(self.get_sceneMapping(
                scId, sceneNumber, wordsTotal, lettersTotal)))

            firstSceneInChapter = False

        return lines, sceneNumber, wordsTotal, lettersTotal

    def get_chapters(self):
        """Process the chapters and nested scenes.
        Return a list of strings.
        """
        lines = []
        chapterNumber = 0
        sceneNumber = 0
        wordsTotal = 0
        lettersTotal = 0

        for chId in self.srtChapters:

            # The order counts; be aware that "Todo" and "Notes" chapters are
            # always unused.

            # Has the chapter only scenes not to be exported?

            sceneCount = 0
            notExportCount = 0
            doNotExport = False

            for scId in self.chapters[chId].srtScenes:
                sceneCount += 1

                if self.scenes[scId].doNotExport:
                    notExportCount += 1

            if sceneCount > 0 and notExportCount == sceneCount:
                doNotExport = True

            if self.chapters[chId].chType == 2:

                if self.todoChapterTemplate != '':
                    template = Template(self.todoChapterTemplate)

                else:
                    continue

            elif self.chapters[chId].chType == 1 or self.chapters[chId].oldType == 1:
                # Chapter is "Notes" (new file format) or "Info" (old file
                # format) chapter.

                if self.notesChapterTemplate != '':
                    template = Template(self.notesChapterTemplate)

                else:
                    continue

            elif self.chapters[chId].isUnused:

                if self.unusedChapterTemplate != '':
                    template = Template(self.unusedChapterTemplate)

                else:
                    continue

            elif doNotExport:

                if self.notExportedChapterTemplate != '':
                    template = Template(self.notExportedChapterTemplate)

                else:
                    continue

            elif self.chapters[chId].chLevel == 1 and self.partTemplate != '':
                template = Template(self.partTemplate)

            else:
                template = Template(self.chapterTemplate)
                chapterNumber += 1

            lines.append(template.safe_substitute(
                self.get_chapterMapping(chId, chapterNumber)))

            # Process scenes.

            sceneLines, sceneNumber, wordsTotal, lettersTotal = self.get_scenes(
                chId, sceneNumber, wordsTotal, lettersTotal, doNotExport)
            lines.extend(sceneLines)

            # Process chapter ending.

            if self.chapters[chId].chType == 2 and self.todoChapterEndTemplate != '':
                lines.append(self.todoChapterEndTemplate)

            elif self.chapters[chId].chType == 1 or self.chapters[chId].oldType == 1:

                if self.notesChapterEndTemplate != '':
                    lines.append(self.notesChapterEndTemplate)

            elif self.chapters[chId].isUnused and self.unusedChapterEndTemplate != '':
                lines.append(self.unusedChapterEndTemplate)

            elif doNotExport and self.notExportedChapterEndTemplate != '':
                lines.append(self.notExportedChapterEndTemplate)

            elif self.chapterEndTemplate != '':
                lines.append(self.chapterEndTemplate)

        return lines

    def get_characters(self):
        """Process the characters.
        Return a list of strings.
        """
        lines = []

        for crId in self.srtCharacters:
            template = Template(self.characterTemplate)
            lines.append(template.safe_substitute(
                self.get_characterMapping(crId)))

        return lines

    def get_locations(self):
        """Process the locations.
        Return a list of strings.
        """
        lines = []

        for lcId in self.srtLocations:
            template = Template(self.locationTemplate)
            lines.append(template.safe_substitute(
                self.get_locationMapping(lcId)))

        return lines

    def get_items(self):
        """Process the items.
        Return a list of strings.
        """
        lines = []

        for itId in self.srtItems:
            template = Template(self.itemTemplate)
            lines.append(template.safe_substitute(self.get_itemMapping(itId)))

        return lines

    def get_text(self):
        """Assemple the whole text applying the templates.
        Return a string to be written to the output file.
        """
        lines = self.get_fileHeader()

        lines.extend(self.get_chapters())
        lines.extend(self.get_characters())
        lines.extend(self.get_locations())
        lines.extend(self.get_items())

        lines.append(self.fileFooter)

        return ''.join(lines)

    def write(self):
        """Create a template-based output file. 
        Return a message string starting with 'SUCCESS' or 'ERROR'.
        """
        text = self.get_text()

        try:
            with open(self.filePath, 'w', encoding='utf-8') as f:
                f.write(text)

        except:
            return 'ERROR: Cannot write "' + os.path.normpath(self.filePath) + '".'

        return 'SUCCESS: "' + os.path.normpath(self.filePath) + '" written.'
