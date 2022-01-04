"""Provide a helper class for scene and chapter splitting.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.model.chapter import Chapter
from pywriter.model.scene import Scene


class Splitter():

    PART_SEPARATOR = '# '
    CHAPTER_SEPARATOR = '## '
    SCENE_SEPARATOR = '* * *'
    # This is used for splitting scenes.

    def split_scenes(self, ywPrj):
        """Generate new chapters and scenes if there are dividers within the scene content.
        """

        def create_chapter(chapterId, title, desc, level):
            """Create a new chapter and add it to the novel.
            """
            newChapter = Chapter()
            newChapter.title = title
            newChapter.desc = desc
            newChapter.chLevel = level
            newChapter.chType = 0
            ywPrj.chapters[chapterId] = newChapter

        def create_scene(sceneId, parent):
            """Create a new scene and add it to the novel.
            """
            WARNING = ' (!) '

            newScene = Scene()

            if parent.desc and not parent.title.endswith(' (split)'):
                parent.title += ' (split)'

            newScene.title = parent.title

            if parent.desc and not parent.desc.startswith(WARNING):
                parent.desc = WARNING + parent.desc

            newScene.desc = parent.desc

            if parent.goal and not parent.goal.startswith(WARNING):
                parent.goal = WARNING + parent.goal

            newScene.goal = parent.goal

            if parent.conflict and not parent.conflict.startswith(WARNING):
                parent.conflict = WARNING + parent.conflict

            newScene.conflict = parent.conflict

            if parent.outcome and not parent.outcome.startswith(WARNING):
                parent.outcome = WARNING + parent.outcome

            newScene.outcome = parent.outcome

            newScene.status = parent.status
            newScene.isNotesScene = parent.isNotesScene
            newScene.isUnused = parent.isUnused
            newScene.isTodoScene = parent.isTodoScene
            newScene.date = parent.date
            newScene.time = parent.time
            newScene.day = parent.day
            newScene.hour = parent.hour
            newScene.minute = parent.minute
            newScene.lastsDays = parent.lastsDays
            newScene.lastsHours = parent.lastsHours
            newScene.lastsMinutes = parent.lastsMinutes
            ywPrj.scenes[sceneId] = newScene

        # Get the maximum chapter ID and scene ID.

        chIdMax = 0
        scIdMax = 0

        for chId in ywPrj.srtChapters:

            if int(chId) > chIdMax:
                chIdMax = int(chId)

        for scId in ywPrj.scenes:

            if int(scId) > scIdMax:
                scIdMax = int(scId)

        srtChapters = []

        for chId in ywPrj.srtChapters:
            srtChapters.append(chId)
            chapterId = chId
            srtScenes = []

            for scId in ywPrj.chapters[chId].srtScenes:
                srtScenes.append(scId)

                if not ywPrj.scenes[scId].sceneContent:
                    continue

                sceneId = scId
                lines = ywPrj.scenes[scId].sceneContent.split('\n')
                newLines = []
                inScene = True

                # Search scene content for dividers.

                for line in lines:

                    if line.startswith(self.PART_SEPARATOR):

                        if inScene:
                            ywPrj.scenes[sceneId].sceneContent = '\n'.join(newLines)
                            newLines = []
                            inScene = False

                        ywPrj.chapters[chapterId].srtScenes = srtScenes
                        srtScenes = []

                        chIdMax += 1
                        chapterId = str(chIdMax)
                        create_chapter(chapterId, 'New part', line.replace(self.PART_SEPARATOR, ''), 1)
                        srtChapters.append(chapterId)

                    elif line.startswith(self.CHAPTER_SEPARATOR):

                        if inScene:
                            ywPrj.scenes[sceneId].sceneContent = '\n'.join(newLines)
                            newLines = []
                            inScene = False

                        ywPrj.chapters[chapterId].srtScenes = srtScenes
                        srtScenes = []

                        chIdMax += 1
                        chapterId = str(chIdMax)
                        create_chapter(chapterId, 'New chapter', line.replace(self.CHAPTER_SEPARATOR, ''), 0)
                        srtChapters.append(chapterId)

                    elif line.startswith(self.SCENE_SEPARATOR):
                        ywPrj.scenes[sceneId].sceneContent = '\n'.join(newLines)
                        newLines = []
                        scIdMax += 1
                        sceneId = str(scIdMax)
                        create_scene(sceneId, ywPrj.scenes[scId])
                        srtScenes.append(sceneId)
                        inScene = True

                    elif not inScene:
                        newLines.append(line)
                        scIdMax += 1
                        sceneId = str(scIdMax)
                        create_scene(sceneId, ywPrj.scenes[scId])
                        srtScenes.append(sceneId)
                        inScene = True

                    else:
                        newLines.append(line)

                ywPrj.scenes[sceneId].sceneContent = '\n'.join(newLines)

            ywPrj.chapters[chapterId].srtScenes = srtScenes

        ywPrj.srtChapters = srtChapters
