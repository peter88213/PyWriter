"""Import and export ywriter7 scenes for proofing.

Proof reading file format = DOCX (Office Open XML format)

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys
import os
import re
from abc import abstractmethod
from abc import ABC


class PywProject(ABC):
    """ Abstract yWriter project representation. """

    class Chapter():
        """ yWriter chapter representation. """

        def __init__(self):
            self.title = ''
            self.type = ''
            self.scenes = []

    class Scene():
        """ yWriter scene representation. """

        def __init__(self):
            self.title = ''
            self.desc = ''
            self._wordCount = 0
            self._letterCount = 0
            self._sceneContent = ''

        @property
        def sceneContent(self):
            return(self._sceneContent)

        @sceneContent.setter
        def sceneContent(self, text):
            """ set sceneContent updating word count and letter count. """
            self._sceneContent = text

            text = re.sub('\[.+?\]|\.|\,| -', '', self._sceneContent)
            # Remove yw7 raw markup for word count
            wordList = text.split()
            self._wordCount = len(wordList)

            text = re.sub('\[.+?\]', '', self._sceneContent)
            # Remove yw7 raw markup for letter count
            text = text.replace('\n', '')
            text = text.replace('\r', '')
            self._letterCount = len(text)

        def isEmpty(self):
            return(self._sceneContent == ' ')

    def __init__(self):
        """ Read data from yw7 project file. """
        self.title = ''
        self.chapters = {}
        self.scenes = {}
        self._cdataTags = ['Title', 'AuthorName', 'Bio', 'Desc', 'FieldTitle1', 'FieldTitle2', 'FieldTitle3', 'FieldTitle4',
                           'LaTeXHeaderFile', 'Tags', 'AKA', 'ImageFile', 'FullName', 'Goals', 'Notes', 'RTFFile', 'SceneContent']

    def get_text(self):
        """ Assemble all scenes in the right order as plain text. """

        text = ''
        for chID in self.chapters:
            text = text + '\n\n' + self.chapters[chID].title + '\n\n'
            for scID in self.chapters[chID].scenes:
                try:
                    text = text + self.scenes[scID].sceneContent + '\n'
                except(TypeError):
                    text = text + '\n'
        text = re.sub('\[.+?\]', '', text)
        return(text)

    def getStructure(self):
        """ Assemble a comparable structure tree. """

        text = ''
        for chID in self.chapters:
            text = text + 'ChID:' + str(chID) + '\n'
            for scID in self.chapters[chID].scenes:
                text = text + '  ScID:' + str(scID) + '\n'
        return(text)


class PywPrjFile(PywProject, ABC):
    """ Abstract yWriter project file representation. """

    _fileExtension = ''

    def __init__(self, filePath):
        PywProject.__init__(self)
        self.filePath = filePath

    @property
    def filePath(self):
        return(self._filePath)

    @filePath.setter
    def filePath(self, filePath):
        """ Accept only filenames with the right extension. """
        fileName = os.path.split(filePath)[1]
        fileName = fileName.lower()
        # Possibly Windows specific
        if fileName.count(self._fileExtension):
            self._filePath = filePath

    @abstractmethod
    def read(self):
        """ Read yWriter project data from a file. """
        pass

    @abstractmethod
    def write(self):
        """ Write yWriter project data to a file. """
        pass

    def file_is_present(self):
        """ Check whether the file is present. """
        if os.path.isfile(self._filePath):
            return(True)
        else:
            return(False)

MD_HEADING_MARKERS = ("##", "#")
# Index is yWriter's chapter type:
# 0 is for an ordinary chapter
# 1 is for a chapter beginning a section


class MdProject(PywPrjFile):
    """ yWriter project linked to a markdown file. """

    _fileExtension = 'md'

    def read(self):
        """ Read data from markdown project file. """

        def format_yw7(text):
            """ Convert markdown to yw7 raw markup. """
            text = text.replace('\r', '\n')
            text = text.replace('\n\n', '\n')
            text = text.replace('\[', '[')
            text = text.replace('\]', ']')
            text = text.replace('\\*', '_asterisk_')
            text = re.sub('\*\*(.+?)\*\*', '[b]\g<1>[/b]', text)
            text = re.sub('\*(.+?)\*', '[i]\g<1>[/i]', text)
            text = text.replace('_asterisk_', '*')
            return(text)

        try:
            with open(self._filePath, 'r', encoding='utf-8') as f:
                text = (f.read())
        except(FileNotFoundError):
            return('ERROR: "' + self._filePath + '" not found.')

        text = format_yw7(text)

        sceneText = ''
        scID = ''
        chID = ''
        inScene = False

        lines = text.split('\n')
        for line in lines:
            if line.count('[ScID'):
                scID = re.search('[0-9]+', line).group()
                self.scenes[scID] = self.Scene()
                self.chapters[chID].scenes.append(scID)
                inScene = True
            elif line.count('[/ScID]'):
                self.scenes[scID].sceneContent = sceneText
                sceneText = ''
                inScene = False
            elif line.count('[ChID'):
                chID = re.search('[0-9]+', line).group()
                self.chapters[chID] = self.Chapter()
            elif line.count('[/ChID]'):
                pass
            elif inScene:
                sceneText = sceneText + line + '\n'
        return('SUCCESS: ' + str(len(self.scenes)) + ' Scenes read from "' + self._filePath + '".')

    def get_text(self):
        """ Format project text to markdown. """

        def format_chapter_title(text):
            """ Fix auto-chapter titles for non-English """
            text = text.replace('Chapter ', '')
            return(text)

        def format_md(text):
            """ Convert yw7 specific markup """
            text = text.replace('\n\n', '\n')
            text = text.replace('\n', '\n\n')
            text = text.replace('*', '\*')
            text = text.replace('[i]', '*')
            text = text.replace('[/i]', '*')
            text = text.replace('[b]', '**')
            text = text.replace('[/b]', '**')
            return(text)

        text = ''
        for chID in self.chapters:
            text = text + '\\[ChID:' + chID + '\\]\n'
            headingMarker = MD_HEADING_MARKERS[self.chapters[chID].type]
            text = text + headingMarker + \
                format_chapter_title(self.chapters[chID].title) + '\n'
            for scID in self.chapters[chID].scenes:
                text = text + '\\[ScID:' + scID + '\\]\n'
                try:
                    text = text + self.scenes[scID].sceneContent + '\n'
                except(TypeError):
                    text = text + '\n'
                text = text + '\\[/ScID\\]\n'
            text = text + '\\[/ChID\\]\n'
        text = format_md(text)
        return(text)

    def write(self):
        """ Write attributes to markdown project file. """

        with open(self._filePath, 'w', encoding='utf-8') as f:
            f.write(self.get_text())

        return('SUCCESS: ' + str(len(self.scenes)) + ' Scenes written to "' + self._filePath + '".')
import xml.etree.ElementTree as ET


class Yw7Project(PywPrjFile):
    """ yWriter project linked to an yw7 project file. """

    def read(self):
        """ Read data from yw7 project file. """
        try:
            # Empty scenes will crash the xml parser, so put a blank in them.
            with open(self._filePath, 'r', encoding='utf-8') as f:
                xmlData = f.read()
        except(FileNotFoundError):
            sys.exit('ERROR: "' + self._filePath + '" not found.')

        if xmlData.count('<![CDATA[]]>'):
            xmlData = xmlData.replace('<![CDATA[]]>', '<![CDATA[ ]]>')
            try:
                with open(self._filePath, 'w', encoding='utf-8') as f:
                    f.write(xmlData)
            except(PermissionError):
                sys.exit('ERROR: "' + self._filePath +
                         '" is write protected.')

        lines = xmlData.split('\n')

        for line in lines:
            # Complete list of tags requiring CDATA (if incomplete)
            tag = re.search('\<(.+?)\>\<\!\[CDATA', line)
            if tag:
                if not (tag.group(1) in self._cdataTags):
                    self._cdataTags.append(tag.group(1))

        try:
            self.tree = ET.parse(self._filePath)
            root = self.tree.getroot()
        except:
            sys.exit('ERROR: Can not process "' + self._filePath + '".')

        for prj in root.iter('PROJECT'):
            self.title = prj.find('Title').text

        for chp in root.iter('CHAPTER'):
            chID = chp.find('ID').text
            self.chapters[chID] = self.Chapter()
            self.chapters[chID].title = chp.find('Title').text
            self.chapters[chID].type = int(chp.find('Type').text)
            self.chapters[chID].scenes = []
            if chp.find('Scenes'):
                for scn in chp.find('Scenes').findall('ScID'):
                    self.chapters[chID].scenes.append(scn.text)

        for scn in root.iter('SCENE'):
            scID = scn.find('ID').text
            self.scenes[scID] = self.Scene()
            self.scenes[scID].title = scn.find('Title').text
            if scn.find('Desc'):
                self.scenes[scID].desc = scn.find('Desc').text
            self.scenes[scID]._sceneContent = scn.find('SceneContent').text

        return('SUCCESS: ' + str(len(self.scenes)) + ' Scenes read from "' + self._filePath + '".')

    def write(self):
        """ Write attributes to yw7 project file. """
        sceneCount = 0
        root = self.tree.getroot()

        for prj in root.iter('PROJECT'):
            prj.find('Title').text = self.title

        for chp in root.iter('CHAPTER'):
            chID = chp.find('ID').text
            chp.find('Title').text = self.chapters[chID].title
            chp.find('Type').text = str(self.chapters[chID].type)
            if chp.find('Scenes'):
                i = 0
                for scn in chp.find('Scenes').findall('ScID'):
                    scn.text = self.chapters[chID].scenes[i]
                    i = i + 1

        for scn in root.iter('SCENE'):
            scID = scn.find('ID').text
            try:
                if self.scenes[scID].isEmpty():
                    scn.find('SceneContent').text = ''
                    scn.find('WordCount').text = '0'
                    scn.find('LetterCount').text = '0'
                else:
                    scn.find(
                        'SceneContent').text = self.scenes[scID]._sceneContent
                    scn.find('WordCount').text = str(
                        self.scenes[scID]._wordCount)
                    scn.find('LetterCount').text = str(
                        self.scenes[scID]._letterCount)
                scn.find('Title').text = self.scenes[scID].title
                if scn.find('Desc'):
                    scn.find('Desc').text = self.scenes[scID].desc
                sceneCount = sceneCount + 1
            except(KeyError):
                return('ERROR: Scene with ID:' + scID + ' is missing in input file - yWriter project not modified.')

        if sceneCount != len(self.scenes):
            return('ERROR: Scenes total mismatch - yWriter project not modified.')

        try:
            self.tree.write(self._filePath, encoding='utf-8')
        except(PermissionError):
            return('ERROR: "' + self._filePath + '" is write protected.')

        newXml = ['<?xml version="1.0" encoding="utf-8"?>\n']
        # try:
        with open(self._filePath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                for tag in self._cdataTags:
                    line = re.sub('\<' + tag + '\>', '<' +
                                  tag + '><![CDATA[', line)
                    line = re.sub('\<\/' + tag + '\>',
                                  ']]></' + tag + '>', line)
                newXml.append(line)
        # except:
        #    return('ERROR: Can not read"' + self._filePath + '".')
        try:
            with open(self._filePath, 'w', encoding='utf-8') as f:
                f.writelines(newXml)
        except:
            return('ERROR: Can not write"' + self._filePath + '".')

        return('SUCCESS: ' + str(sceneCount) + ' Scenes written to "' + self._filePath + '".')


class MdConverter():

    def __init__(self, yw7File, mdFile):
        self.yw7File = yw7File
        self.yw7Prj = Yw7Project(self.yw7File)
        self.mdFile = mdFile
        self.mdPrj = MdProject(self.mdFile)

    def yw7_to_md(self):
        """ Read .yw7 file and convert xml to markdown. """
        if not self.yw7Prj.filePath:
            return('ERROR: "' + self.yw7File + '" is not an yWriter 7 project.')

        if not self.yw7Prj.file_is_present():
            return('ERROR: Project "' + self.yw7File + '" not found.')
        else:
            self.confirm_overwrite(self.yw7File)

        message = self.yw7Prj.read()
        if message.count('ERROR'):
            return(message)

        self.mdPrj.title = self.yw7Prj.title
        self.mdPrj.scenes = self.yw7Prj.scenes
        self.mdPrj.chapters = self.yw7Prj.chapters
        return(self.mdPrj.write())

    def md_to_yw7(self):
        """ Convert markdown to xml and replace .yw7 file. """
        if not self.yw7Prj.filePath:
            return('ERROR: "' + self.yw7File + '" is not an yWriter 7 project.')

        if not self.yw7Prj.file_is_present():
            return('ERROR: Project "' + self.yw7File + '" not found.')
        else:
            self.confirm_overwrite(self.yw7File)

        message = self.yw7Prj.read()
        if message.count('ERROR'):
            return(message)

        if not self.mdPrj.filePath:
            return('ERROR: "' + self.mdFile + '" is not a Markdown file.')

        if not self.mdPrj.file_is_present():
            return('ERROR: "' + self.mdFile + '" not found.')

        message = self.mdPrj.read()
        if message.count('ERROR'):
            return(message)

        prjStructure = self.mdPrj.getStructure()
        if prjStructure == '':
            return('ERROR: Source file contains no yWriter project structure information.')

        if prjStructure != self.yw7Prj.getStructure():
            return('ERROR: Structure mismatch - yWriter project not modified.')

        for scID in self.mdPrj.scenes:
            self.yw7Prj.scenes[scID].sceneContent = self.mdPrj.scenes[scID].sceneContent

        return(self.yw7Prj.write())

    def confirm_overwrite(self, fileName):
        pass


def convert_file(srcFile, dstFormat, format='', outputfile='', extra_args=[]):
    """ Pandoc wrapper emulating the pypandoc.convert_file functon. """

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
            return(result)




class DocumentConverter(MdConverter):

    mdFile = 'temp.md'
    _fileExtensions = ['docx', 'html', 'odt']

    def __init__(self, yw7File, documentFile):
        MdConverter.__init__(self, yw7File, self.mdFile)
        self.documentFile = documentFile
        nameParts = self.documentFile.split('.')
        self.fileExtension = nameParts[len(nameParts) - 1]

    @property
    def fileExtension(self):
        return(self._fileExtension)

    @fileExtension.setter
    def fileExtension(self, fileExt):
        if fileExt in self._fileExtensions:
            self._fileExtension = fileExt

    def yw7_to_document(self):
        """ Export to document """
        message = self.yw7_to_md()
        if message.count('ERROR'):
            return(message)

        if os.path.isfile(self.documentFile):
            self.confirm_overwrite(self.documentFile)

        try:
            os.remove(self.documentFile)
        except(FileNotFoundError):
            pass
        convert_file(self.mdFile, self.fileExtension, format='markdown_strict',
                     outputfile=self.documentFile)
        # Let pandoc convert markdown and write to .document file.
        os.remove(self.mdFile)
        if os.path.isfile(self.documentFile):
            return(message.replace(self.mdFile, self.documentFile))

        else:
            return('ERROR: Could not create "' + self.documentFile + '".')

    def document_to_yw7(self):
        """ Import from yw7 """
        convert_file(self.documentFile, 'markdown_strict', format=self._fileExtension,
                     outputfile=self.mdFile, extra_args=['--wrap=none'])
        # Let pandoc read the document file and convert to markdown.
        message = self.md_to_yw7()
        try:
            os.remove(self.mdFile)
        except(FileNotFoundError):
            pass
        return(message)


class MyDocxConverter(DocumentConverter):

    def __init__(self, yw7File, docxFile, silentMode=True):
        DocumentConverter.__init__(self, yw7File, docxFile)
        self.silentMode = silentMode

    def confirm_overwrite(self, file):
        if not self.silentMode:
            print('\nWARNING: This will overwrite "' +
                  file + '"!')
            userConfirmation = input('Continue (y/n)? ')
            if not userConfirmation in ('y', 'Y'):
                print('Program abort by user.\n')
                input('Press ENTER to continue ...')
                sys.exit(1)


def run(sourcePath, silentMode=True):
    """ File conversion for proofreading """
    sourceFile = os.path.split(sourcePath)
    pathToSource = sourceFile[0]
    if pathToSource:
        pathToSource = pathToSource + '/'

    if sourceFile[1].count('.yw7'):
        yw7File = pathToSource + sourceFile[1]
        docxFile = pathToSource + \
            sourceFile[1].split('.yw7')[0] + '.docx'
        myConverter = MyDocxConverter(yw7File, docxFile, silentMode)
        print('\n*** Export yWriter7 scenes to .docx ***')
        print('Project: "' + yw7File + '"')
        print(myConverter.yw7_to_docx())

    elif sourceFile[1].count('.docx'):
        docxFile = pathToSource + sourceFile[1]
        yw7File = pathToSource + \
            sourceFile[1].split('.docx')[0] + '.yw7'
        myConverter = MyDocxConverter(yw7File, docxFile, silentMode)
        print('\n*** Import yWriter7 scenes from .docx ***')
        print('Proofed scenes in "' + docxFile + '"')
        print(myConverter.docx_to_yw7())

    else:
        print('Input file must be .yw7 or .docx type.')

    if not silentMode:
        input('Press ENTER to continue ...')


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]
    except:
        print(__doc__)
        sys.exit(1)

    run(sourcePath, False)
