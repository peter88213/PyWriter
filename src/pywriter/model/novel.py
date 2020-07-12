"""Novel - represents the basic structure of an yWriter project.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from abc import abstractmethod
import os
from string import Template

from pywriter.model.character import Character
from pywriter.model.object import Object
from pywriter.model.scene import Scene
from pywriter.model.chapter import Chapter


class Novel():
    """Abstract yWriter project file representation.

    This class represents a file containing a novel with additional 
    attributes and structural information (a full set or a subset
    of the information included in an yWriter project file).
    """

    fileHeader = ''
    chapterTemplate = ''
    sceneTemplate = ''
    sceneDivider = ''
    characterTemplate = ''
    locationTemplate = ''
    itemTemplate = ''
    fileFooter = ''
    _FILE_EXTENSION = ''
    # To be extended by file format specific subclasses.

    def __init__(self, filePath):
        self.title = None
        # str
        # xml: <PROJECT><Title>

        self.desc = None
        # str
        # xml: <PROJECT><Desc>

        self.author = None
        # str
        # xml: <PROJECT><AuthorName>

        self.fieldTitle1 = None
        # str
        # xml: <PROJECT><FieldTitle1>

        self.fieldTitle2 = None
        # str
        # xml: <PROJECT><FieldTitle2>

        self.fieldTitle3 = None
        # str
        # xml: <PROJECT><FieldTitle3>

        self.fieldTitle4 = None
        # str
        # xml: <PROJECT><FieldTitle4>

        self.chapters = {}
        # dict
        # xml: <CHAPTERS><CHAPTER><ID>
        # key = chapter ID, value = Chapter object.
        # The order of the elements does not matter (the novel's
        # order of the chapters is defined by srtChapters)

        self.scenes = {}
        # dict
        # xml: <SCENES><SCENE><ID>
        # key = scene ID, value = Scene object.
        # The order of the elements does not matter (the novel's
        # order of the scenes is defined by the order of the chapters
        # and the order of the scenes within the chapters)

        self.srtChapters = []
        # list of str
        # The novel's chapter IDs. The order of its elements
        # corresponds to the novel's order of the chapters.

        self.locations = {}
        # dict
        # xml: <LOCATIONS>
        # key = location ID, value = Object.
        # The order of the elements does not matter.

        self.items = {}
        # dict
        # xml: <ITEMS>
        # key = item ID, value = Object.
        # The order of the elements does not matter.

        self.characters = {}
        # dict
        # xml: <CHARACTERS>
        # key = character ID, value = Character object.
        # The order of the elements does not matter.

        self._filePath = None
        # str
        # Path to the file. The setter only accepts files of a
        # supported type as specified by _FILE_EXTENSION.

        self.filePath = filePath

    @property
    def filePath(self):
        return self._filePath

    @filePath.setter
    def filePath(self, filePath):
        """Accept only filenames with the right extension. """
        if filePath.lower().endswith(self._FILE_EXTENSION):
            self._filePath = filePath

    @abstractmethod
    def read(self):
        """Parse the file and store selected properties.
        To be overwritten by file format specific subclasses.
        """

    def convert_markup(self, text):
        """Convert yw7 markup to target format.
        To be overwritten by file format specific subclasses.
        """

        if text is None:
            text = ''

        return(text)

    @abstractmethod
    def merge(self, novel):
        """Merge selected novel properties.
        To be overwritten by file format specific subclasses.
        """

    def write(self):
        lines = []
        wordsTotal = 0
        lettersTotal = 0
        chapterNumber = 0
        sceneNumber = 0

        # Append html header template and fill in.

        projectTemplateSubst = dict(
            Title=self.title,
            Desc=self.convert_markup(self.desc),
            AuthorName=self.author,
            FieldTitle1=self.fieldTitle1,
            FieldTitle2=self.fieldTitle2,
            FieldTitle3=self.fieldTitle3,
            FieldTitle4=self.fieldTitle4,
        )

        template = Template(self.fileHeader)
        lines.append(template.safe_substitute(projectTemplateSubst))

        for chId in self.srtChapters:

            if self.chapters[chId].isUnused:
                continue

            if self.chapters[chId].chType != 0:
                continue

            chapterNumber += 1

            # Append chapter template and fill in.

            chapterSubst = dict(
                ID=chId,
                ChapterNumber=chapterNumber,
                Title=self.chapters[chId].title,
                Desc=self.convert_markup(self.chapters[chId].desc),
            )

            template = Template(self.chapterTemplate)
            lines.append(template.safe_substitute(chapterSubst))

            firstSceneInChapter = True

            for scId in self.chapters[chId].srtScenes:
                wordsTotal += self.scenes[scId].wordCount
                lettersTotal += self.scenes[scId].letterCount

                if self.scenes[scId].isUnused:
                    continue

                if self.scenes[scId].doNotExport:
                    continue

                sceneNumber += 1

                if not (firstSceneInChapter or self.scenes[scId].appendToPrev):
                    lines.append(self.sceneDivider)

                # Prepare data for substitution.

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

                # Append scene template and fill in.

                sceneSubst = dict(
                    ID=scId,
                    SceneNumber=sceneNumber,
                    Title=self.scenes[scId].title,
                    Desc=self.convert_markup(self.scenes[scId].desc),
                    WordCount=str(self.scenes[scId].wordCount),
                    WordsTotal=wordsTotal,
                    LetterCount=str(self.scenes[scId].letterCount),
                    LettersTotal=lettersTotal,
                    Status=Scene.STATUS[self.scenes[scId].status],
                    SceneContent=self.convert_markup(
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
                    Goal=self.convert_markup(self.scenes[scId].goal),
                    Conflict=self.convert_markup(self.scenes[scId].conflict),
                    Outcome=self.convert_markup(self.scenes[scId].outcome),
                    Tags=tags,
                    Characters=sceneChars,
                    Viewpoint=viewpointChar,
                    Locations=sceneLocs,
                    Items=sceneItems,
                    Notes=self.convert_markup(self.scenes[scId].sceneNotes),
                )

                template = Template(self.sceneTemplate)
                lines.append(template.safe_substitute(sceneSubst))

                firstSceneInChapter = False

        for crId in self.characters:

            # Prepare data for substitution.

            if self.characters[crId].tags is not None:
                tags = ', '.join(self.characters[crId].tags)

            else:
                tags = ''

            if self.characters[crId].isMajor:
                characterStatus = Character.MAJOR_MARKER

            else:
                characterStatus = Character.MINOR_MARKER

            # Append character template and fill in.

            characterSubst = dict(
                ID=crId,
                Title=self.characters[crId].title,
                Desc=self.convert_markup(self.characters[crId].desc),
                Tags=tags,
                AKA=Novel.convert_markup(self, self.characters[crId].aka),
                Notes=self.convert_markup(self.characters[crId].notes),
                Bio=self.convert_markup(self.characters[crId].bio),
                Goals=self.convert_markup(self.characters[crId].goals),
                FullName=Novel.convert_markup(
                    self, self.characters[crId].fullName),
                Status=characterStatus,
            )

            template = Template(self.characterTemplate)
            lines.append(template.safe_substitute(characterSubst))

        for lcId in self.locations:

            # Prepare data for substitution.

            if self.locations[lcId].tags is not None:
                tags = ', '.join(self.locations[lcId].tags)

            else:
                tags = ''

            # Append location template and fill in.

            locationSubst = dict(
                ID=lcId,
                Title=self.locations[lcId].title,
                Desc=self.convert_markup(self.locations[lcId].desc),
                Tags=tags,
                AKA=Novel.convert_markup(self, self.locations[lcId].aka),
            )

            template = Template(self.locationTemplate)
            lines.append(template.safe_substitute(locationSubst))

        for itId in self.items:

            # Prepare data for substitution.

            if self.items[itId].tags is not None:
                tags = ', '.join(self.items[itId].tags)

            else:
                tags = ''

            # Append item template and fill in.

            itemSubst = dict(
                ID=itId,
                Title=self.items[itId].title,
                Desc=self.convert_markup(self.items[itId].desc),
                Tags=tags,
                AKA=Novel.convert_markup(self, self.items[itId].aka),
            )

            template = Template(self.itemTemplate)
            lines.append(template.safe_substitute(itemSubst))

        # Append html footer and fill in.

        lines.append(self.fileFooter)
        text = ''.join(lines)

        try:
            with open(self.filePath, 'w', encoding='utf-8') as f:
                f.write(text)

        except:
            return 'ERROR: Cannot write "' + self.filePath + '".'

        return 'SUCCESS: Content written to "' + self.filePath + '".'

    def file_exists(self):
        """Check whether the file specified by _filePath exists. """
        if os.path.isfile(self._filePath):
            return True

        else:
            return False

    def get_structure(self):
        """returns a string showing the order of chapters and scenes 
        as a tree. The result can be used to compare two Novel objects 
        by their structure.
        """
        lines = []

        for chId in self.srtChapters:
            lines.append('ChID:' + str(chId) + '\n')

            for scId in self.chapters[chId].srtScenes:
                lines.append('  ScID:' + str(scId) + '\n')

        return ''.join(lines)
