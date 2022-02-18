"""Provide a class for yWriter scene representation.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import re


class Scene():
    """yWriter scene representation.
    
    Public instance variables:
        title -- scene title.
        desc -- scene description in a single string.
        sceneContent -- scene content in a single string (property with getter and setter).
        rtfFile -- RTF file name (yWriter 5).
        wordCount - word count (updated by the sceneContent setter).
        letterCount - letter count (updated by the sceneContent setter).
        isUnused -- True if the scene is marked "Unused". 
        isNotesScene -- True if the scene type is "Notes".
        isTodoScene -- True if the scene type is "Todo". 
        doNotExport -- True if the scene is not to be exported to RTF.
        status -- scene status (Outline/Draft/1st Edit/2nd Edit/Done).
        sceneNotes -- scene notes in a single string.
        tags -- list of scene tags. 
        field1 -- scene ratings field 1.
        field2 -- scene ratings field 2.
        field3 -- scene ratings field 3.
        field4 -- scene ratings field 4.
        appendToPrev -- If True, append the scene without a divider to the previous scene.
        isReactionScene -- If True, the scene is "reaction". Otherwise, it's "action". 
        isSubPlot -- If True, the scene belongs to a sub-plot. Otherwise it's main plot.  
        goal -- The main actor's scene goal. 
        conflict -- What hinders the main actor to achieve his goal.
        outcome -- What comes out at the end of the scene.
        characters -- list of character IDs related to this scene.
        locations -- list of location IDs related to this scene. 
        items -- list of item IDs related to this scene.
        date -- specific start date in ISO format (yyyy-mm-dd).
        time -- specific start time in ISO format (hh:mm).
        minute -- unspecific start time: minutes.
        hour -- unspecific start time: hour.
        day -- unspecific start time: day.
        lastsMinutes -- scene duration: minutes.
        lastsHours -- scene duration: hours.
        lastsDays -- scene duration: days. 
        image -- Path to an image related to the scene. 
    """

    # Emulate an enumeration for the scene status
    # Since the items are used to replace text,
    # they may contain spaces. This is why Enum cannot be used here.

    STATUS = (None, 'Outline', 'Draft', '1st Edit', '2nd Edit', 'Done')
    ACTION_MARKER = 'A'
    REACTION_MARKER = 'R'

    NULL_DATE = '0001-01-01'
    NULL_TIME = '00:00:00'

    def __init__(self):
        """Initialize instance variables."""
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

        self.rtfFile = None
        # str
        # xml: <RTFFile>
        # Name of the file containing the scene in yWriter 5.

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

        self.isNotesScene = None
        # bool
        # xml: <Fields><Field_SceneType> 1

        self.isTodoScene = None
        # bool
        # xml: <Fields><Field_SceneType> 2

        self.doNotExport = None
        # bool
        # xml: <ExportCondSpecific><ExportWhenRTF>

        self.status = None
        # int
        # xml: <Status>
        # 1 - Outline
        # 2 - Draft
        # 3 - 1st Edit
        # 4 - 2nd Edit
        # 5 - Done
        # See also the STATUS list for conversion.

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

        self.image = None
        # str
        # xml: <ImageFile>

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
