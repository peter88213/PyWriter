"""Merge two yWriter projects.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from pywriter.model.chapter import Chapter
from pywriter.model.scene import Scene
from pywriter.model.character import Character
from pywriter.model.object import Object


class YwProjectMerger():
    """Merge two yWriter projects."""

    def merge_projects(self, target, source):
        """Overwrite existing target attributes with source attributes.
        Create target attributes, if not existing, but return ERROR.
        Return a message beginning with SUCCESS or ERROR.
        """

        mismatchCount = 0

        # Merge locations.

        for lcId in source.locations:

            if not lcId in target.locations:
                target.locations[lcId] = Object()
                mismatchCount += 1

            if source.locations[lcId].title:
                # avoids deleting the title, if it is empty by accident
                target.locations[lcId].title = source.locations[lcId].title

            if source.locations[lcId].desc is not None:
                target.locations[lcId].desc = source.locations[lcId].desc

            if source.locations[lcId].aka is not None:
                target.locations[lcId].aka = source.locations[lcId].aka

            if source.locations[lcId].tags is not None:
                target.locations[lcId].tags = source.locations[lcId].tags

        # Merge items.

        for itId in source.items:

            if not itId in target.items:
                target.items[itId] = Object()
                mismatchCount += 1

            if source.items[itId].title:
                # avoids deleting the title, if it is empty by accident
                target.items[itId].title = source.items[itId].title

            if source.items[itId].desc is not None:
                target.items[itId].desc = source.items[itId].desc

            if source.items[itId].aka is not None:
                target.items[itId].aka = source.items[itId].aka

            if source.items[itId].tags is not None:
                target.items[itId].tags = source.items[itId].tags

        # Merge characters.

        for crId in source.characters:

            if not crId in target.characters:
                target.characters[crId] = Character()
                mismatchCount += 1

            if source.characters[crId].title:
                # avoids deleting the title, if it is empty by accident
                target.characters[crId].title = source.characters[crId].title

            if source.characters[crId].desc is not None:
                target.characters[crId].desc = source.characters[crId].desc

            if source.characters[crId].aka is not None:
                target.characters[crId].aka = source.characters[crId].aka

            if source.characters[crId].tags is not None:
                target.characters[crId].tags = source.characters[crId].tags

            if source.characters[crId].notes is not None:
                target.characters[crId].notes = source.characters[crId].notes

            if source.characters[crId].bio is not None:
                target.characters[crId].bio = source.characters[crId].bio

            if source.characters[crId].goals is not None:
                target.characters[crId].goals = source.characters[crId].goals

            if source.characters[crId].fullName is not None:
                target.characters[crId].fullName = source.characters[crId].fullName

            if source.characters[crId].isMajor is not None:
                target.characters[crId].isMajor = source.characters[crId].isMajor

        # Merge scenes.

        for scId in source.scenes:

            if not scId in target.scenes:
                target.scenes[scId] = Scene()
                mismatchCount += 1

            if source.scenes[scId].title:
                # avoids deleting the title, if it is empty by accident
                target.scenes[scId].title = source.scenes[scId].title

            if source.scenes[scId].desc is not None:
                target.scenes[scId].desc = source.scenes[scId].desc

            if source.scenes[scId].sceneContent is not None:
                target.scenes[scId].sceneContent = source.scenes[scId].sceneContent

            if source.scenes[scId].rtfFile is not None:
                target.scenes[scId].sceneContent = source.scenes[scId].sceneContent

            if source.scenes[scId].isUnused is not None:
                target.scenes[scId].isUnused = source.scenes[scId].isUnused

            if source.scenes[scId].isNotesScene is not None:
                target.scenes[scId].isNotesScene = source.scenes[scId].isNotesScene

            if source.scenes[scId].isTodoScene is not None:
                target.scenes[scId].isTodoScene = source.scenes[scId].isTodoScene

            if source.scenes[scId].status is not None:
                target.scenes[scId].status = source.scenes[scId].status

            if source.scenes[scId].sceneNotes is not None:
                target.scenes[scId].sceneNotes = source.scenes[scId].sceneNotes

            if source.scenes[scId].tags is not None:
                target.scenes[scId].tags = source.scenes[scId].tags

            if source.scenes[scId].field1 is not None:
                target.scenes[scId].field1 = source.scenes[scId].field1

            if source.scenes[scId].field2 is not None:
                target.scenes[scId].field2 = source.scenes[scId].field2

            if source.scenes[scId].field3 is not None:
                target.scenes[scId].field3 = source.scenes[scId].field3

            if source.scenes[scId].field4 is not None:
                target.scenes[scId].field4 = source.scenes[scId].field4

            if source.scenes[scId].appendToPrev is not None:
                target.scenes[scId].appendToPrev = source.scenes[scId].appendToPrev

            if source.scenes[scId].date is not None:
                target.scenes[scId].date = source.scenes[scId].date

            if source.scenes[scId].time is not None:
                target.scenes[scId].time = source.scenes[scId].time

            if source.scenes[scId].minute is not None:
                target.scenes[scId].minute = source.scenes[scId].minute

            if source.scenes[scId].hour is not None:
                target.scenes[scId].hour = source.scenes[scId].hour

            if source.scenes[scId].day is not None:
                target.scenes[scId].day = source.scenes[scId].day

            if source.scenes[scId].lastsMinutes is not None:
                target.scenes[scId].lastsMinutes = source.scenes[scId].lastsMinutes

            if source.scenes[scId].lastsHours is not None:
                target.scenes[scId].lastsHours = source.scenes[scId].lastsHours

            if source.scenes[scId].lastsDays is not None:
                target.scenes[scId].lastsDays = source.scenes[scId].lastsDays

            if source.scenes[scId].isReactionScene is not None:
                target.scenes[scId].isReactionScene = source.scenes[scId].isReactionScene

            if source.scenes[scId].isSubPlot is not None:
                target.scenes[scId].isSubPlot = source.scenes[scId].isSubPlot

            if source.scenes[scId].goal is not None:
                target.scenes[scId].goal = source.scenes[scId].goal

            if source.scenes[scId].conflict is not None:
                target.scenes[scId].conflict = source.scenes[scId].conflict

            if source.scenes[scId].outcome is not None:
                target.scenes[scId].outcome = source.scenes[scId].outcome

            if source.scenes[scId].characters is not None:
                target.scenes[scId].characters = []

                for crId in source.scenes[scId].characters:

                    if crId in target.characters:
                        target.scenes[scId].characters.append(crId)

            if source.scenes[scId].locations is not None:
                target.scenes[scId].locations = []

                for lcId in source.scenes[scId].locations:

                    if lcId in target.locations:
                        target.scenes[scId].locations.append(lcId)

            if source.scenes[scId].items is not None:
                target.scenes[scId].items = []

                for itId in source.scenes[scId].items:

                    if itId in target.items:
                        target.scenes[scId].append(itId)

        # Merge chapters.

        scenesAssigned = []

        for chId in source.chapters:

            if not chId in target.chapters:
                target.chapters[chId] = Chapter()
                mismatchCount += 1

            if source.chapters[chId].title:
                # avoids deleting the title, if it is empty by accident
                target.chapters[chId].title = source.chapters[chId].title

            if source.chapters[chId].desc is not None:
                target.chapters[chId].desc = source.chapters[chId].desc

            if source.chapters[chId].chLevel is not None:
                target.chapters[chId].chLevel = source.chapters[chId].chLevel

            if source.chapters[chId].oldType is not None:
                target.chapters[chId].oldType = source.chapters[chId].oldType

            if source.chapters[chId].chType is not None:
                target.chapters[chId].chType = source.chapters[chId].chType

            if source.chapters[chId].isUnused is not None:
                target.chapters[chId].isUnused = source.chapters[chId].isUnused

            if source.chapters[chId].suppressChapterTitle is not None:
                target.chapters[chId].suppressChapterTitle = source.chapters[chId].suppressChapterTitle

            if source.chapters[chId].suppressChapterBreak is not None:
                target.chapters[chId].suppressChapterBreak = source.chapters[chId].suppressChapterBreak

            if source.chapters[chId].isTrash is not None:
                target.chapters[chId].isTrash = source.chapters[chId].isTrash

            if source.chapters[chId].srtScenes is not None:
                target.chapters[chId].srtScenes = []

                for scId in source.chapters[chId].srtScenes:

                    if (scId in target.scenes) and not (scId in scenesAssigned):
                        target.chapters[chId].srtScenes.append(scId)
                        scenesAssigned.append(scId)

        # Merge attributes at novel level.

        if source.title:
            # avoids deleting the title, if it is empty by accident
            target.title = source.title

        if source.desc is not None:
            target.desc = source.desc

        if source.author is not None:
            target.author = source.author

        if source.fieldTitle1 is not None:
            target.fieldTitle1 = source.fieldTitle1

        if source.fieldTitle2 is not None:
            target.fieldTitle2 = source.fieldTitle2

        if source.fieldTitle3 is not None:
            target.fieldTitle3 = source.fieldTitle3

        if source.fieldTitle4 is not None:
            target.fieldTitle4 = source.fieldTitle4

        if source.srtChapters != []:
            target.srtChapters = []

            for chId in source.srtChapters:
                target.srtChapters.append(chId)

        if mismatchCount > 0:
            return 'ERROR: Project structure mismatch.'

        else:
            return 'SUCCESS'
