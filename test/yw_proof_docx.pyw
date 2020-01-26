"""Import and export ywriter7 scenes for proofing. 

Proof reading file format: DOCX (Office Open XML format) with visible chapter and scene tags.

Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import sys


import os



class Novel():
    """yWriter project representation. 

    # Attributes

    title : str
        the novel title.

    desc : str
        the novel summary.

    chapters : dict 
        key = chapter ID, value = Chapter object.
        The order of the elements does not matter (the novel's 
        order of the chapters is defined by srtChapters)

    scenes : dict
        key = scene ID, value = Scene object.
        The order of the elements does not matter (the novel's 
        order of the scenes is defined by the order of the chapters 
        and the order of the scenes within the chapters)

    srtChapters : list 
        the novel's chapter IDs. The order of its elements 
        corresponds to the novel's order of the chapters.

    # Methods 

    get_structure : str
        returns a string showing the order of chapters and scenes as 
        a tree. The result can be used to compare two Novel objects 
        by their structure.
    """

    def __init__(self) -> None:
        self.title = ''
        self.desc = ''
        self.chapters = {}
        self.scenes = {}
        self.srtChapters = []

    def get_structure(self) -> str:
        """Assemble a comparable structure tree. """

        lines = []
        for chId in self.srtChapters:
            lines.append('ChID:' + str(chId) + '\n')
            for scId in self.chapters[chId].srtScenes:
                lines.append('  ScID:' + str(scId) + '\n')
        return ''.join(lines)



def convert_file(srcFile: str, dstFormat: str, format: str = '', outputfile: str = '', extra_args: list = []) -> str:
    """Pandoc wrapper emulating the pypandoc.convert_file functon. """

    temporaryFile = 'temp.txt'

    extraArgs = ' '
    for extraArgument in extra_args:
        extraArgs = extraArgs + extraArgument + ' '

    if outputfile != '':
        dstFile = outputfile
    else:
        dstFile = temporaryFile

    argument1 = 'pandoc'
    argument2 = ' -w ' + dstFormat
    argument3 = ' -r ' + format
    argument4 = ' -o "' + dstFile + '"'
    argument5 = ' ' + extraArgs
    argument6 = ' "' + srcFile + '"'

    status = os.system(argument1 + argument2 + argument3 +
                       argument4 + argument5 + argument6)

    if status == 0:

        if outputfile == '':

            with open(temporaryFile, 'r', encoding='utf-8') as f:
                result = f.read()

            os.remove(temporaryFile)
            return result



import re


from abc import abstractmethod, ABC



class PywFile(Novel, ABC):
    """Abstract yWriter project file representation.

    This class represents a file containing a novel with additional 
    attributes and structural information (a full set or a subset
    of the information included in an yWriter project file).

    # Properties

    filePath : str (property with setter)
        Path to the file.
        The setter only accepts files of a supported type as specified 
        by _FILE_EXTENSION. 

    # Methods

    read : str
        Abstract method for parsing the file and writing selected 
        properties to the novel.

    write : str
        Arguments
            novel : Novel
                the data to be written. 
        Abstract method for writing selected novel properties to the file.

    file_exists() : bool
        True means: the file specified by filePath exists. 
    """

    _FILE_EXTENSION = ''
    # To be extended by file format specific subclasses.

    def __init__(self, filePath: str) -> None:
        Novel.__init__(self)
        self._filePath = None
        self.filePath = filePath

    @property
    def filePath(self) -> str:
        return self._filePath

    @filePath.setter
    def filePath(self, filePath: str) -> None:
        """Accept only filenames with the right extension. """
        if filePath.lower().endswith(self._FILE_EXTENSION):
            self._filePath = filePath

    @abstractmethod
    def read(self) -> None:
        """Parse the file and store selected properties. """
        # To be overwritten by file format specific subclasses.

    @abstractmethod
    def write(self, novel: Novel):
        """Write selected novel properties to the file. """
        # To be overwritten by file format specific subclasses.

    def file_exists(self) -> bool:
        """Check whether the file specified by _filePath exists. """

        if os.path.isfile(self._filePath):
            return True

        else:
            return False


class Chapter():
    """yWriter chapter representation.

    # Attributes

    title : str
        the chapter title.

    desc : str
        the chapter summary.

    chLevel : int
        a selector for the heading.
        0 = chapter level
        1 = section level (marked "begins a section")

    chType : int
        0 = chapter type (marked "Ch")
        1 = other type (marked "I")

    isUnused : bool
        the chapter is marked "unused".

    srtScenes : list 
        the chapter's scene IDs. The order of its elements 
        corresponds to the chapter's order of the scenes.
    """

    def __init__(self) -> None:
        self.title = ''
        self.desc = ''
        self.chLevel = 0
        self.chType = None
        self.isUnused = False
        self.srtScenes = []



class Scene():
    """yWriter scene representation.

    # Attributes

    title : str
        the scene title.

    desc : str
        scene summary.

    sceneContent : str (property with setter)
        scene text with raw markup.

    wordCount : int 
        (to be updated by the sceneContent setter).

    letterCount : int 
        (to be updated by the sceneContent setter).

    isUnused : bool
        the scene is marked "unused".

    # Methods 

    isEmpty : bool
        True means: the scene is defined, but has no content.
    """

    def __init__(self):
        self.title = ''
        self.desc = ''
        self.wordCount = 0
        self.letterCount = 0
        self.isUnused = False
        self._sceneContent = ''

    @property
    def sceneContent(self) -> str:
        return self._sceneContent

    @sceneContent.setter
    def sceneContent(self, text: str) -> None:
        """Set sceneContent updating word count and letter count. """

        self._sceneContent = text
        text = re.sub('\[.+?\]|\.|\,| -', '', self._sceneContent)
        # Remove yw7 raw markup for word count

        wordList = text.split()
        self.wordCount = len(wordList)

        text = re.sub('\[.+?\]', '', self._sceneContent)
        # Remove yw7 raw markup for letter count

        text = text.replace('\n', '')
        text = text.replace('\r', '')
        self.letterCount = len(text)

    def isEmpty(self) -> bool:
        """Check whether the scene has no content yet. """

        return self._sceneContent == ' '

MD_HEADING_MARKERS = ("##", "#")
# Index is yWriter's chapter chLevel:
# 0 is for an ordinary chapter
# 1 is for a chapter beginning a section


class MdFile(PywFile):
    """Markdown file representation of an yWriter project's OfficeFile part. 

    Represents a Markdown file with visible chapter and scene tags 
    to be converted by Pandoc.

    # Attributes

    _text : str
        contains the parsed data.

    _collectText : bool
        simple parsing state indicator. 
        True means: the data returned by the html parser 
        belongs to the body section. 

    # Methods

    read : str
        parse the Markdown file located at filePath, fetching 
        the Novel attributes.
        Return a message beginning with SUCCESS or ERROR. 

    write : str
        Arguments 
            novel : Novel
                the data to be written. 
        Generate a Markdown file containing:
        - chapter ID tags,
        - chapter headings,
        - scene ID tags, 
        - scene content.
        Return a message beginning with SUCCESS or ERROR.
    """

    _FILE_EXTENSION = 'md'
    # overwrites PywFile._FILE_EXTENSION

    def read(self) -> str:
        """Read data from markdown file with chapter and scene tags. """

        def to_yw7(text: str) -> str:
            """Convert markdown to yw7 raw markup. """

            text = text.replace('<sub>', '')
            text = text.replace('</sub>', '')
            # html tags misplaced by Pandoc.
            text = text.replace('\r', '\n')
            text = text.replace('\n\n', '\n')
            text = text.replace('\[', '[')
            text = text.replace('\]', ']')
            text = text.replace('\\*', '_asterisk_')
            text = re.sub('\*\*(.+?)\*\*', '[b]\g<1>[/b]', text)
            text = re.sub('\*(.+?)\*', '[i]\g<1>[/i]', text)
            text = text.replace('_asterisk_', '*')
            return text

        try:
            with open(self._filePath, 'r', encoding='utf-8') as f:
                text = (f.read())

        except(FileNotFoundError):
            return 'ERROR: "' + self._filePath + '" not found.'

        text = to_yw7(text)

        sceneText = []
        scId = ''
        chId = ''
        inScene = False

        lines = text.split('\n')

        for line in lines:

            if line.startswith('[ScID'):
                scId = re.search('[0-9]+', line).group()
                self.scenes[scId] = Scene()
                self.chapters[chId].srtScenes.append(scId)
                inScene = True

            elif line.startswith('[/ScID'):
                self.scenes[scId].sceneContent = ''.join(sceneText)
                sceneText = []
                inScene = False

            elif line.startswith('[ChID'):
                chId = re.search('[0-9]+', line).group()
                self.chapters[chId] = Chapter()
                self.srtChapters.append(chId)

            elif line.startswith('[/ChID'):
                pass

            elif inScene:
                sceneText.append(line + '\n')

        return 'SUCCESS: ' + str(len(self.scenes)) + ' Scenes read from "' + self._filePath + '".'

    def write(self, novel: Novel) -> str:
        """Write novel attributes to Markdown file. """

        def format_chapter_title(text: str) -> str:
            """Fix auto-chapter titles for non-English. """

            text = text.replace('Chapter ', '')
            return text

        def to_md(text: str) -> str:
            """Convert yw7 specific markup. """

            text = text.replace('\n\n', '\n')
            text = text.replace('\n', '\n\n')
            text = text.replace('*', '\*')
            text = text.replace('[i]', '*')
            text = text.replace('[/i]', '*')
            text = text.replace('[b]', '**')
            text = text.replace('[/b]', '**')
            return text

        # Copy the novel's attributes to write

        if novel.srtChapters != []:
            self.srtChapters = novel.srtChapters

        if novel.scenes is not None:
            self.scenes = novel.scenes

        if novel.chapters is not None:
            self.chapters = novel.chapters

        lines = []

        for chId in self.srtChapters:

            if self.chapters[chId].isUnused:
                lines.append('\\[ChID:' + chId + ' (Unused)\\]\n')

            else:
                lines.append('\\[ChID:' + chId + '\\]\n')

            headingMarker = MD_HEADING_MARKERS[self.chapters[chId].chLevel]
            lines.append(headingMarker +
                         format_chapter_title(self.chapters[chId].title) + '\n')

            for scId in self.chapters[chId].srtScenes:

                if self.scenes[scId].isUnused:
                    lines.append('\\[ScID:' + scId + ' (Unused)\\]\n')

                else:
                    lines.append('\\[ScID:' + scId + '\\]\n')

                try:
                    lines.append(self.scenes[scId].sceneContent + '\n')

                except(TypeError):
                    lines.append('\n')

                if self.scenes[scId].isUnused:
                    lines.append('\\[/ScID (Unused)\\]\n')

                else:
                    lines.append('\\[/ScID\\]\n')

            if self.chapters[chId].isUnused:
                lines.append('\\[/ChID (Unused)\\]\n')

            else:
                lines.append('\\[/ChID\\]\n')

        text = to_md(''.join(lines))

        try:
            with open(self._filePath, 'w', encoding='utf-8') as f:
                f.write(text)

        except(PermissionError):
            return 'ERROR: ' + self._filePath + '" is write protected.'

        return 'SUCCESS: "' + self._filePath + '" saved.'


class OfficeFile(MdFile):
    """Office file representation.

    Represents an Office text document with visible chapter and scene tags 
    to be converted by Pandoc.

    # Properties

    filePath : str (property with setter)
        Path to the office document file for Pandoc operation.
        The setter only accepts files of a supported type as listed
        in _FILE_EXTENSIONS. 
        For reading and writing the intermediate Markdown file,
        this attribute is temporarily overwritten with the 
        path to the intermediate file. 

    # Methods

    read : str
        let pandoc read the document file and convert to markdown.
        parse the Markdown file, fetching the Novel attributes.
        Return a message beginning with SUCCESS or ERROR. 

    write : str
        Arguments
            novel : Novel
                the data to be written. 
        Generate an intermediate Markdown file containing:
        - chapter ID tags,
        - chapter headings,
        - scene ID tags, 
        - scene content.
        Let Pandoc convert this Markdown file into the target format.
        Return a message beginning with SUCCESS or ERROR.
    """

    _FILE_EXTENSIONS = ['docx', 'odt']

    def __init__(self, filePath: str) -> None:
        MdFile.__init__(self, 'temp.md')
        self._filePath = None
        self.filePath = filePath
        self._tempFile = 'temp.md'

    @property
    def filePath(self) -> str:
        return self._filePath

    @filePath.setter
    def filePath(self, documentPath: str) -> None:
        nameParts = documentPath.split('.')
        fileExt = nameParts[len(nameParts) - 1]
        if fileExt in self._FILE_EXTENSIONS:
            self._FILE_EXTENSION = fileExt
            self._filePath = documentPath

    def read(self) -> str:
        """Generate and read a temporary Markdown file. """

        if not os.path.isfile(self.filePath):
            return 'ERROR: "' + self.filePath + '" not found.'

        # Let pandoc read the document file and convert to markdown.

        convert_file(self.filePath, 'markdown_strict', format=self._FILE_EXTENSION,
                     outputfile=self._tempFile, extra_args=['--wrap=none'])

        documentPath = self._filePath
        self._filePath = self._tempFile
        message = MdFile.read(self)
        self._filePath = documentPath
        os.remove(self._tempFile)

        if message.startswith('ERROR'):
            return message

        return 'SUCCESS: ' + str(len(self.scenes)) + ' Scenes read from "' + self._filePath + '".'

    def write(self, novel: Novel) -> str:
        """Write to a temporary Markdown file and convert it into an office document. """

        documentPath = self._filePath
        self._filePath = self._tempFile
        message = MdFile.write(self, novel)
        self._filePath = documentPath

        if message.startswith('ERROR'):
            return message

        try:
            os.remove(self.filePath)

        except(FileNotFoundError):
            pass

        # Let pandoc convert markdown and write to the document.

        convert_file(self._tempFile, self._FILE_EXTENSION, format='markdown_strict',
                     outputfile=self.filePath)

        os.remove(self._tempFile)

        if os.path.isfile(self.filePath):
            return message.replace(self._tempFile, self.filePath)

        else:
            return 'ERROR: Could not create "' + self.filePath + '".'

from tkinter import *
from tkinter import messagebox


import xml.etree.ElementTree as ET



class Yw7File(PywFile):
    """yWriter 7 xml project file representation.

    # Attributes

    _cdataTags : list of str
        names of yw7 xml elements containing CDATA. 
        ElementTree.write omits CDATA tags, so they have to be 
        inserted afterwards. 

    # Methods

    read : str
        parse the yw7 xml file located at filePath, fetching the 
        Novel attributes.
        Return a message beginning with SUCCESS or ERROR. 

    write : str
        Arguments 
            novel : Novel
                the data to be written. 
        Open the yw7 xml file located at filePath and replace a set 
        of items by the novel attributes not being None.
        Return a message beginning with SUCCESS or ERROR.

    is_locked : bool
        tests whether a .lock file placed by yWriter exists.
    """

    _FILE_EXTENSION = '.yw7'
    # overwrites PywFile._FILE_EXTENSION

    def __init__(self, filePath: str) -> None:
        PywFile.__init__(self, filePath)
        self._cdataTags = ['Title', 'AuthorName', 'Bio', 'Desc', 'FieldTitle1', 'FieldTitle2', 'FieldTitle3', 'FieldTitle4',
                           'LaTeXHeaderFile', 'Tags', 'AKA', 'ImageFile', 'FullName', 'Goals', 'Notes', 'RTFFile', 'SceneContent']

    def read(self) -> str:
        """Parse yw7 xml project file and store selected attributes. """

        # Complete list of tags requiring CDATA (if incomplete).

        try:
            with open(self._filePath, 'r', encoding='utf-8') as f:
                xmlData = f.read()

        except(FileNotFoundError):
            return 'ERROR: "' + self._filePath + '" not found.'

        lines = xmlData.split('\n')

        for line in lines:
            tag = re.search('\<(.+?)\>\<\!\[CDATA', line)

            if tag is not None:

                if not (tag.group(1) in self._cdataTags):
                    self._cdataTags.append(tag.group(1))

        # Open the file again and let ElementTree parse its xml structure.

        try:
            self.tree = ET.parse(self._filePath)
            root = self.tree.getroot()

        except:
            return 'ERROR: Can not process "' + self._filePath + '".'

        for prj in root.iter('PROJECT'):
            self.title = prj.find('Title').text
            self.desc = prj.find('Desc').text

        for chp in root.iter('CHAPTER'):
            chId = chp.find('ID').text
            self.chapters[chId] = Chapter()
            self.chapters[chId].title = chp.find('Title').text
            self.srtChapters.append(chId)

            if chp.find('Desc') is not None:
                self.chapters[chId].desc = chp.find('Desc').text

            if chp.find('SectionStart') is not None:
                self.chapters[chId].chLevel = 1

            if chp.find('Unused') is not None:
                self.chapters[chId].isUnused = True

            self.chapters[chId].chType = int(chp.find('Type').text)

            self.chapters[chId].srtScenes = []

            if chp.find('Scenes') is not None:

                for scn in chp.find('Scenes').findall('ScID'):
                    scId = scn.text
                    self.chapters[chId].srtScenes.append(scId)

        for scn in root.iter('SCENE'):
            scId = scn.find('ID').text

            self.scenes[scId] = Scene()
            self.scenes[scId].title = scn.find('Title').text

            if scn.find('Desc') is not None:
                self.scenes[scId].desc = scn.find('Desc').text

            if scn.find('Unused') is not None:
                self.scenes[scId].isUnused = True

            sceneContent = scn.find('SceneContent').text

            if sceneContent is not None:
                self.scenes[scId].sceneContent = sceneContent

        return 'SUCCESS: ' + str(len(self.scenes)) + ' Scenes read from "' + self._filePath + '".'

    def write(self, novel: Novel) -> str:
        """Write novel's attributes to yw7 project file. """

        # Copy the novel's attributes to write

        if novel.title != '':
            self.title = novel.title

        if novel.srtChapters != []:
            self.srtChapters = novel.srtChapters

        if novel.scenes is not None:

            for scId in novel.scenes:

                if novel.scenes[scId].title != '':
                    self.scenes[scId].title = novel.scenes[scId].title

                if novel.scenes[scId].desc != '':
                    self.scenes[scId].desc = novel.scenes[scId].desc

                if novel.scenes[scId].sceneContent != '':
                    self.scenes[scId].sceneContent = novel.scenes[scId].sceneContent

                '''Do not modify these items yet:
                if novel.scenes[scId].isUnused is not None:
                    self.scenes[scId].isUnused = novel.chapters[chId].isUnused
                '''

        if novel.chapters is not None:

            for chId in novel.chapters:

                if novel.chapters[chId].title != '':
                    self.chapters[chId].title = novel.chapters[chId].title

                if novel.chapters[chId].desc != '':
                    self.chapters[chId].desc = novel.chapters[chId].desc

                '''Do not modify these items yet:
                if novel.chapters[chId].chLevel is not None:
                    self.chapters[chId].chLevel = novel.chapters[chId].chLevel

                if novel.chapters[chId].chType is not None:
                    self.chapters[chId].chType = novel.chapters[chId].chType

                if novel.chapters[chId].isUnused is not None:
                    self.chapters[chId].isUnused = novel.chapters[chId].isUnused

                if novel.chapters[chId].srtScenes != []:
                    self.chapters[chId].srtScenes = novel.chapters[chId].srtScenes
                '''

        sceneCount = 0
        root = self.tree.getroot()

        for prj in root.iter('PROJECT'):
            prj.find('Title').text = self.title

        for chp in root.iter('CHAPTER'):
            chId = chp.find('ID').text

            if chId in self.chapters:
                chp.find('Title').text = self.chapters[chId].title

                if self.chapters[chId].desc != '':

                    if chp.find('Desc') is None:
                        newDesc = ET.SubElement(chp, 'Desc')
                        newDesc.text = self.chapters[chId].desc

                    else:
                        chp.find('Desc').text = self.chapters[chId].desc

                '''Do not modify these items yet:
                chp.find('Type').text = str(self.chapters[chId].chType)
                
                levelInfo = chp.find('SectionStart')
                
                if levelInfo is not None:
                    
                    if self.chapters[chId].chLevel == 0:
                         chp.remove(levelInfo)

                unusedMarker = chp.find('Unused')
                
                if unused is not None:
                    
                    if not self.chapters[chId].isUnused:
                         chp.remove(unusedMarker)
                '''

        for scn in root.iter('SCENE'):

            scId = scn.find('ID').text

            if scId in self.scenes:

                if self.scenes[scId].isEmpty():
                    scn.find('SceneContent').text = ''
                    scn.find('WordCount').text = '0'
                    scn.find('LetterCount').text = '0'

                else:
                    scn.find(
                        'SceneContent').text = self.scenes[scId]._sceneContent
                    scn.find('WordCount').text = str(
                        self.scenes[scId].wordCount)
                    scn.find('LetterCount').text = str(
                        self.scenes[scId].letterCount)

                scn.find('Title').text = self.scenes[scId].title

                if self.scenes[scId].desc != '':
                    if scn.find('Desc') is None:
                        newDesc = ET.SubElement(scn, 'Desc')
                        newDesc.text = self.scenes[scId].desc

                    else:
                        scn.find('Desc').text = self.scenes[scId].desc

                '''Do not modify these items yet:
                unusedMarker = scn.find('Unused')
                
                if unused is not None:
                    
                    if not self.scenes[scId].isUnused:
                         scn.remove(unusedMarker)
                '''

                sceneCount = sceneCount + 1

        try:
            self.tree.write(self._filePath, encoding='utf-8')

        except(PermissionError):
            return 'ERROR: "' + self._filePath + '" is write protected.'

        # Postprocess the xml file created by ElementTree:
        # Put a header on top and insert the missing CDATA tags.

        newXml = '<?xml version="1.0" encoding="utf-8"?>\n'
        with open(self._filePath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

            for line in lines:

                for tag in self._cdataTags:
                    line = re.sub('\<' + tag + '\>', '<' +
                                  tag + '><![CDATA[', line)
                    line = re.sub('\<\/' + tag + '\>',
                                  ']]></' + tag + '>', line)

                newXml = newXml + line

        newXml = newXml.replace('\n \n', '\n')
        newXml = newXml.replace('[CDATA[ \n', '[CDATA[')
        newXml = newXml.replace('\n]]', ']]')

        try:
            with open(self._filePath, 'w', encoding='utf-8') as f:
                f.write(newXml)

        except:
            return 'ERROR: Can not write"' + self._filePath + '".'

        return 'SUCCESS: ' + str(sceneCount) + ' Scenes written to "' + self._filePath + '".'

    def is_locked(self) -> bool:

        if os.path.isfile(self._filePath + '.lock'):
            return True

        else:
            return False


UNSTRUCTURED = ['ChapterDesc', 'PartDesc', 'CsvFile']
# File classes without a chapter/scene tree structure.


class Yw7Cnv():
    """Converter for yWriter 7 project files.

    # Methods

    yw7_to_document : str
        Arguments
            yw7File : Yw7File
                an object representing the source file.
            documentFile : PywFile
                a PywFile subclass instance representing the target file.
        read .yw7 file, parse xml and create a document file.
        Return a message beginning with SUCCESS or ERROR.    

    document_to_yw7 : str
        Arguments
            documentFile : PywFile
                a PywFile subclass instance representing the source file.
            yw7File : Yw7File
                an object representing the target file.
        read document file, convert its content to xml, and replace .yw7 file.
        Return a message beginning with SUCCESS or ERROR.

    confirm_overwrite : bool
        Arguments
            fileName : str
                Path to the file to be overwritten
        ask for permission to overwrite the target file.
        Returns True by default.
        This method is to be overwritten by subclasses with an user interface.
    """

    def yw7_to_document(self, yw7File: Yw7File, documentFile: PywFile) -> str:
        """Read .yw7 file and convert xml to a document file. """

        if yw7File.is_locked():
            return 'ERROR: yWriter 7 seems to be open. Please close first.'

        if yw7File.filePath is None:
            return 'ERROR: "' + yw7File.filePath + '" is not an yWriter 7 project.'

        message = yw7File.read()

        if message.startswith('ERROR'):
            return message

        if documentFile.file_exists():

            if not self.confirm_overwrite(documentFile.filePath):
                return 'Program abort by user.'

        return documentFile.write(yw7File)

    def document_to_yw7(self, documentFile: PywFile, yw7File: Yw7File) -> str:
        """Read document file, convert its content to xml, and replace .yw7 file. """

        if yw7File.is_locked():
            return 'ERROR: yWriter 7 seems to be open. Please close first.'

        if yw7File.filePath is None:
            return 'ERROR: "' + yw7File.filePath + '" is not an yWriter 7 project.'

        if not yw7File.file_exists():
            return 'ERROR: Project "' + yw7File.filePath + '" not found.'

        else:

            if not self.confirm_overwrite(yw7File.filePath):
                return 'Program abort by user.'

        if documentFile.filePath is None:
            return 'ERROR: "' + documentFile.filePath + '" is not of the supported type.'

        if not documentFile.file_exists():
            return 'ERROR: "' + documentFile.filePath + '" not found.'

        message = documentFile.read()

        if message.startswith('ERROR'):
            return message

        prjStructure = documentFile.get_structure()

        message = yw7File.read()
        # initialize yw7File data

        if message.startswith('ERROR'):
            return message

        if not documentFile.__class__.__name__ in UNSTRUCTURED:

            if prjStructure == '':
                return 'ERROR: Source file contains no yWriter project structure information.'

            if prjStructure != yw7File.get_structure():
                return 'ERROR: Structure mismatch - yWriter project not modified.'

        return yw7File.write(documentFile)

    def confirm_overwrite(self, fileName: str) -> bool:
        return True


TITLE = 'PyWriter v1.2'


class CnvRunner(Yw7Cnv):
    """Standalone yWriter 7 converter with a simple GUI. 

    # Arguments

        sourcePath : str
            a full or relative path to the file to be converted.
            Either an .yw7 file or a file of any supported type. 
            The file type determines the conversion's direction.    

        document : PywFile
            instance of any PywFile subclass representing the 
            source or target document. 

        extension : str
            file extension determining the source or target 
            document's file type. The extension is needed because 
            there can be ambiguous PywFile subclasses 
            (e.g. OfficeFile).
            Examples: 
            - md
            - docx
            - odt
            - html

        silentMode : bool
            True by default. Intended for automated tests. 
            If True, the GUI is not started and no further 
            user interaction is required. Overwriting of existing
            files is forced. 
            Calling scripts shall set silentMode = False.

        suffix : str
            optional file name suffix used for ambiguous html files.
            Examples:
            - _manuscript for a html file containing scene contents.
            - _scenedesc for a html file containing scene descriptions.
            - _chapterdesc for a html file containing chapter descriptions.
    """

    def __init__(self, sourcePath: str,
                 document: PywFile,
                 extension: str,
                 silentMode: bool = True,
                 suffix: str = '') -> None:
        """Run the converter with a GUI. """

        # Prepare the graphical user interface.

        root = Tk()
        root.geometry("800x300")
        root.title(TITLE)
        self.header = Label(root, text=__doc__)
        self.header.pack(padx=5, pady=5)
        self.appInfo = Label(root, text='')
        self.appInfo.pack(padx=5, pady=5)
        self.successInfo = Label(root)
        self.successInfo.pack(fill=X, expand=1, padx=50, pady=5)
        self.processInfo = Label(root, text='')
        self.processInfo.pack(padx=5, pady=5)

        # Run the converter.

        self.silentMode = silentMode
        self.__run(sourcePath, document, extension, suffix)

        # Visualize the outcome.

        if not self.silentMode:
            root.quitButton = Button(text="OK", command=quit)
            root.quitButton.config(height=1, width=10)
            root.quitButton.pack(padx=5, pady=5)
            root.mainloop()

    def __run(self, sourcePath: str,
              document: PywFile,
              extension: str,
              suffix: str) -> None:
        """Determine the direction and invoke the converter. """

        # The conversion's direction depends on the sourcePath argument.

        if sourcePath.endswith('.yw7'):
            yw7Path = sourcePath

            # Generate the target file path.

            document.filePath = sourcePath.split(
                '.yw7')[0] + suffix + '.' + extension
            self.appInfo.config(
                text='Export yWriter7 scenes content to ' + extension)
            self.processInfo.config(text='Project: "' + yw7Path + '"')

            # Instantiate an Yw7File object and pass it along with
            # the document to the converter class.

            yw7File = Yw7File(yw7Path)
            self.processInfo.config(
                text=self.yw7_to_document(yw7File, document))

        elif sourcePath.endswith(suffix + '.' + extension):
            document.filePath = sourcePath

            # Determine the project file path.

            yw7Path = sourcePath.split(suffix + '.' + extension)[0] + '.yw7'
            self.appInfo.config(
                text='Import yWriter7 scenes content from ' + extension)
            self.processInfo.config(
                text='Proofed scenes in "' + document.filePath + '"')

            # Instantiate an Yw7File object and pass it along with
            # the document to the converter class.

            yw7File = Yw7File(yw7Path)
            self.processInfo.config(
                text=self.document_to_yw7(document, yw7File))

        else:
            self.processInfo.config(
                text='Argument is wrong or missing (drag and drop error?)\nInput file must be .yw7 or ' + suffix + '.' + extension + ' type.')
            self.successInfo.config(bg='red')

        # Visualize the outcome.

        if 'ERROR' in self.processInfo.cget('text'):
            self.successInfo.config(bg='red')

        elif 'SUCCESS' in self.processInfo.cget('text'):
            self.successInfo.config(bg='green')

    def confirm_overwrite(self, filePath: str) -> bool:
        """ Invoked by the parent if a file already exists. """

        if self.silentMode:
            return True

        else:
            return messagebox.askyesno('WARNING', 'Overwrite existing file "' + filePath + '"?')


def run(sourcePath: str, silentMode: bool = True) -> None:
    document = OfficeFile('')
    converter = CnvRunner(sourcePath, document, 'docx', silentMode)


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]
    except:
        sourcePath = ''
    run(sourcePath, False)
