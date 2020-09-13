"""FileExport - Generic template-based file exporter.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
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
    """

    fileHeader = ''
    partTemplate = ''
    chapterTemplate = ''
    notesChapterTemplate = ''
    todoChapterTemplate = ''
    unusedChapterTemplate = ''
    sceneTemplate = ''
    appendedSceneTemplate = ''
    notesSceneTemplate = ''
    todoSceneTemplate = ''
    unusedSceneTemplate = ''
    sceneDivider = ''
    chapterEndTemplate = ''
    unusedChapterEndTemplate = ''
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
        """Copy selected novel attributes.
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

        if novel.characters is not None:
            self.characters = novel.characters

        if novel.locations is not None:
            self.locations = novel.locations

        if novel.items is not None:
            self.items = novel.items

        return 'SUCCESS'

    def get_projectTemplateSubst(self):
        projectTemplateSubst = dict(
            Title=self.title,
            Desc=self.convert_from_yw(self.desc),
            AuthorName=self.author,
            FieldTitle1=self.fieldTitle1,
            FieldTitle2=self.fieldTitle2,
            FieldTitle3=self.fieldTitle3,
            FieldTitle4=self.fieldTitle4,
        )

        for key in projectTemplateSubst:
            if projectTemplateSubst[key] is None:
                projectTemplateSubst[key] = ''

        return projectTemplateSubst

    def get_chapterSubst(self, chId, chapterNumber):
        chapterSubst = dict(
            ID=chId,
            ChapterNumber=chapterNumber,
            Title=self.chapters[chId].title,
            Desc=self.convert_from_yw(self.chapters[chId].desc),
            ProjectName=self.projectName,
            ProjectPath=self.projectPath,
        )

        for key in chapterSubst:
            if chapterSubst[key] is None:
                chapterSubst[key] = ''

        return chapterSubst

    def get_sceneSubst(self, scId, sceneNumber, wordsTotal, lettersTotal):

        if self.scenes[scId].tags is not None:
            tags = ', '.join(self.scenes[scId].tags)

        else:
            tags = ''

        if self.scenes[scId].characters is not None:
            sChList = []

            for chId in self.scenes[scId].characters:
                sChList.append(self.characters[chId].title)

            sceneChars = ', '.join(sChList)
            viewpointChar = sChList[0]

        else:
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

        sceneSubst = dict(
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

        for key in sceneSubst:
            if sceneSubst[key] is None:
                sceneSubst[key] = ''

        return sceneSubst

    def get_characterSubst(self, crId):

        if self.characters[crId].tags is not None:
            tags = ', '.join(self.characters[crId].tags)

        else:
            tags = ''

        if self.characters[crId].isMajor:
            characterStatus = Character.MAJOR_MARKER

        else:
            characterStatus = Character.MINOR_MARKER

        characterSubst = dict(
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

        for key in characterSubst:
            if characterSubst[key] is None:
                characterSubst[key] = ''

        return characterSubst

    def get_locationSubst(self, lcId):

        if self.locations[lcId].tags is not None:
            tags = ', '.join(self.locations[lcId].tags)

        else:
            tags = ''

        locationSubst = dict(
            ID=lcId,
            Title=self.locations[lcId].title,
            Desc=self.convert_from_yw(self.locations[lcId].desc),
            Tags=tags,
            AKA=FileExport.convert_from_yw(self, self.locations[lcId].aka),
        )

        for key in locationSubst:
            if locationSubst[key] is None:
                locationSubst[key] = ''

        return locationSubst

    def get_itemSubst(self, itId):

        if self.items[itId].tags is not None:
            tags = ', '.join(self.items[itId].tags)

        else:
            tags = ''

        itemSubst = dict(
            ID=itId,
            Title=self.items[itId].title,
            Desc=self.convert_from_yw(self.items[itId].desc),
            Tags=tags,
            AKA=FileExport.convert_from_yw(self, self.items[itId].aka),
        )

        for key in itemSubst:
            if itemSubst[key] is None:
                itemSubst[key] = ''

        return itemSubst

    def write(self):
        lines = []
        wordsTotal = 0
        lettersTotal = 0
        chapterNumber = 0
        sceneNumber = 0

        template = Template(self.fileHeader)
        lines.append(template.safe_substitute(self.get_projectTemplateSubst()))

        for chId in self.srtChapters:

            # The order counts; be aware that "Todo" and "Notes" chapters are
            # always unused.

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

            elif self.chapters[chId].chLevel == 1 and self.partTemplate != '':
                template = Template(self.partTemplate)

            else:
                template = Template(self.chapterTemplate)
                chapterNumber += 1

            lines.append(template.safe_substitute(
                self.get_chapterSubst(chId, chapterNumber)))
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

                elif self.scenes[scId].isUnused or self.chapters[chId].isUnused or self.scenes[scId].doNotExport:

                    if self.unusedSceneTemplate != '':
                        template = Template(self.unusedSceneTemplate)

                    else:
                        continue

                else:
                    sceneNumber += 1

                    template = Template(self.sceneTemplate)

                    if self.scenes[scId].appendToPrev and self.appendedSceneTemplate != '':
                        template = Template(self.appendedSceneTemplate)

                if not (firstSceneInChapter or self.scenes[scId].appendToPrev):
                    lines.append(self.sceneDivider)

                lines.append(template.safe_substitute(self.get_sceneSubst(
                    scId, sceneNumber, wordsTotal, lettersTotal)))

                firstSceneInChapter = False

            if self.chapters[chId].chType == 2:

                if self.todoChapterEndTemplate != '':
                    lines.append(self.todoChapterEndTemplate)

                else:
                    continue

            elif self.chapters[chId].chType == 1 or self.chapters[chId].oldType == 1:

                if self.notesChapterEndTemplate != '':
                    lines.append(self.notesChapterEndTemplate)

                else:
                    continue

            elif self.chapters[chId].isUnused and self.unusedChapterEndTemplate != '':
                lines.append(self.unusedChapterEndTemplate)

            else:
                lines.append(self.chapterEndTemplate)

        for crId in self.characters:
            template = Template(self.characterTemplate)
            lines.append(template.safe_substitute(
                self.get_characterSubst(crId)))

        for lcId in self.locations:
            template = Template(self.locationTemplate)
            lines.append(template.safe_substitute(
                self.get_locationSubst(lcId)))

        for itId in self.items:
            template = Template(self.itemTemplate)
            lines.append(template.safe_substitute(self.get_itemSubst(itId)))

        lines.append(self.fileFooter)
        text = ''.join(lines)

        try:
            with open(self.filePath, 'w', encoding='utf-8') as f:
                f.write(text)

        except:
            return 'ERROR: Cannot write "' + os.path.normpath(self.filePath) + '".'

        return 'SUCCESS: "' + os.path.normpath(self.filePath) + '" written.'
