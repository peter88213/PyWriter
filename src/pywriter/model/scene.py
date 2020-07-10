"""Scene - represents the basic structure of a scene in yWriter.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import re


class Scene():
    """yWriter scene representation.
    # xml: <SCENES><SCENE>
    """

    # Emulate an enumeration for the scene status

    STATUS = [None, 'Outline', 'Draft', '1st Edit', '2nd Edit', 'Done']

    def __init__(self):
        self.title = None
        # str
        # xml: <Title>

        self.desc = None
        # str
        # xml: <Desc>

        self._sceneContent = None
        # str
        # xml: <SceneContent>
        # Scene text with yW7 raw markup.

        self.wordCount = 0
        # int # xml: <WordCount>
        # To be updated by the sceneContent setter

        self.letterCount = 0
        # int
        # xml: <LetterCount>
        # To be updated by the sceneContent setter

        self.isUnused = None
        # bool
        # xml: <Unused> -1

        self.doNotExport = None
        # bool
        # xml: <ExportCondSpecific><ExportWhenRTF>

        self.status = None
        # int # xml: <Status>

        self.sceneNotes = None
        # str
        # xml: <Notes>

        self.tags = None
        # list of str
        # xml: <Tags>

        self.field1 = None
        # str
        # xml: <Field1>

        self.field2 = None
        # str
        # xml: <Field2>

        self.field3 = None
        # str
        # xml: <Field3>

        self.field4 = None
        # str
        # xml: <Field4>

        self.appendToPrev = None
        # bool
        # xml: <AppendToPrev> -1

        self.isReactionScene = None
        # bool
        # xml: <ReactionScene> -1

        self.isSubPlot = None
        # bool
        # xml: <SubPlot> -1

        self.goal = None
        # str
        # xml: <Goal>

        self.conflict = None
        # str
        # xml: <Conflict>

        self.outcome = None
        # str
        # xml: <Outcome>

        self.characters = None
        # list of str
        # xml: <Characters><CharID>

        self.locations = None
        # list of str
        # xml: <Locations><LocID>

        self.items = None
        # list of str
        # xml: <Items><ItemID>

        self.date = None
        # str
        # xml: <SpecificDateMode>-1
        # xml: <SpecificDateTime>1900-06-01 20:38:00

        self.time = None
        # str
        # xml: <SpecificDateMode>-1
        # xml: <SpecificDateTime>1900-06-01 20:38:00

        self.minute = None
        # str
        # xml: <Minute>

        self.hour = None
        # str
        # xml: <Hour>

        self.day = None
        # str
        # xml: <Day>

        self.lastsMinutes = None
        # str
        # xml: <LastsMinutes>

        self.lastsHours = None
        # str
        # xml: <LastsHours>

        self.lastsDays = None
        # str
        # xml: <LastsDays>

    @property
    def sceneContent(self):
        return self._sceneContent

    @sceneContent.setter
    def sceneContent(self, text):
        """Set sceneContent updating word count and letter count."""
        self._sceneContent = text
        text = re.sub('\[.+?\]|\.|\,| -', '', self._sceneContent)
        # Remove yWriter raw markup for word count

        wordList = text.split()
        self.wordCount = len(wordList)

        text = re.sub('\[.+?\]', '', self._sceneContent)
        # Remove yWriter raw markup for letter count

        text = text.replace('\n', '')
        text = text.replace('\r', '')
        self.letterCount = len(text)

    def merge(self, scene):
        """Merge attributes.
        """

        if scene.title:
            # avoids deleting the title, if it is empty by accident
            self.title = scene.title

        if scene.desc is not None:
            self.desc = scene.desc

        if scene.sceneContent is not None:
            self.sceneContent = scene.sceneContent

        if scene.isUnused is not None:
            self.isUnused = scene.isUnused

        if scene.doNotExport is not None:
            self.doNotExport = scene.doNotExport

        if scene.status is not None:
            self.status = scene.status

        if scene.sceneNotes is not None:
            self.sceneNotes = scene.sceneNotes

        if scene.tags is not None:
            self.tags = scene.tags

        if scene.field1 is not None:
            self.field1 = scene.field1

        if scene.field2 is not None:
            self.field2 = scene.field2

        if scene.field3 is not None:
            self.field3 = scene.field3

        if scene.field4 is not None:
            self.field4 = scene.field4

        if scene.appendToPrev is not None:
            self.appendToPrev = scene.appendToPrev

        if scene.date is not None:
            self.date = scene.date

        if scene.time is not None:
            self.time = scene.time

        if scene.minute is not None:
            self.minute = scene.minute

        if scene.hour is not None:
            self.hour = scene.hour

        if scene.day is not None:
            self.day = scene.day

        if scene.lastsMinutes is not None:
            self.lastsMinutes = scene.lastsMinutes

        if scene.lastsHours is not None:
            self.lastsHours = scene.lastsHours

        if scene.lastsDays is not None:
            self.lastsDays = scene.lastsDays

        if scene.isReactionScene is not None:
            self.isReactionScene = scene.isReactionScene

        if scene.isSubPlot is not None:
            self.isSubPlot = scene.isSubPlot

        if scene.goal is not None:
            self.goal = scene.goal

        if scene.conflict is not None:
            self.conflict = scene.conflict

        if scene.outcome is not None:
            self.outcome = scene.outcome
