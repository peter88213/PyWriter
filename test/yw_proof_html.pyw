"""Import and export ywriter7 scenes for proofing. 

Proof reading file format = html with visible chapter and scene tags.

Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import sys


from html.parser import HTMLParser

from abc import abstractmethod
import os


class Novel():
    """Abstract yWriter project file representation.

    This class represents a file containing a novel with additional 
    attributes and structural information (a full set or a subset
    of the information included in an yWriter project file).
    """

    _FILE_EXTENSION = ''
    # To be extended by file format specific subclasses.

    def __init__(self, filePath):
        self.title = None
        # str

        self.summary = None
        # str

        self.author = None
        # str

        self.fieldTitle1 = None
        # str

        self.fieldTitle2 = None
        # str

        self.fieldTitle3 = None
        # str

        self.fieldTitle4 = None
        # str

        self.chapters = {}
        # key = chapter ID, value = Chapter object.
        # The order of the elements does not matter (the novel's
        # order of the chapters is defined by srtChapters)

        self.scenes = {}
        # key = scene ID, value = Scene object.
        # The order of the elements does not matter (the novel's
        # order of the scenes is defined by the order of the chapters
        # and the order of the scenes within the chapters)

        self.srtChapters = []
        # list of str
        # The novel's chapter IDs. The order of its elements
        # corresponds to the novel's order of the chapters.

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

    @abstractmethod
    def write(self, novel):
        """Write selected novel properties to the file.
        To be overwritten by file format specific subclasses.
        """

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


class Chapter():
    """yWriter chapter representation."""

    def __init__(self):
        self.title = None
        # str

        self.summary = None
        # str

        self.chLevel = None
        # int
        # 0 = chapter level
        # 1 = section level ("this chapter begins a section")

        self.chType = None
        # int
        # 0 = chapter type (marked "Chpter")
        # 1 = other type (marked "Other")

        self.isUnused = None
        # bool

        self.srtScenes = []
        # list of str
        # The chapter's scene IDs. The order of its elements
        # corresponds to the chapter's order of the scenes.

import re


class Scene():
    """yWriter scene representation."""

    def __init__(self):
        self.title = None
        # str

        self.summary = None
        # str

        self._sceneContent = None
        # str
        # Scene text with yW7 raw markup.

        self.wordCount = None
        # int
        # To be updated by the sceneContent setter

        self.letterCount = None
        # int
        # To be updated by the sceneContent setter

        self.isUnused = None
        # bool

        self.tags = None
        # list of str

        self.sceneNotes = None
        # str

        self.field1 = None
        # str

        self.field2 = None
        # str

        self.field3 = None
        # str

        self.field4 = None
        # str

    @property
    def sceneContent(self):
        return self._sceneContent

    @sceneContent.setter
    def sceneContent(self, text):
        """Set sceneContent updating word count and letter count."""
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



HTML_SCENE_DIVIDER = '* * *'
# To be placed between scene ending and beginning tags.

# Make the generated html file look good in a web browser:

STYLESHEET = '<style type="text/css">\n' + \
    'h1, h2, h3, h4, p {font: 1em monospace; margin: 3em; line-height: 1.5em}\n' + \
    'h1, h2, h3, h4 {text-align: center}\n' +\
    'h1 {letter-spacing: 0.2em; font-style: italic}' + \
    'h1, h2 {font-weight: bold}\n' + \
    'h3 {font-style: italic}\n' + \
    'p.textbody {margin-top:0; margin-bottom:0}\n' + \
    'p.firstlineindent {margin-top:0; margin-bottom:0; text-indent: 1em}\n' + \
    'strong {font-weight:normal; text-transform: uppercase}\n' + \
    '</style>\n'

HTML_HEADER = '<html>\n' + '<head>\n' + \
    '<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>\n' + STYLESHEET + \
    '<title>$bookTitle$</title>\n' + \
    '</head>\n' + '<body>\n'

HTML_FOOTER = '\n</body>\n</html>\n'


def to_yw7(text):
    """Convert html tags to yw7 raw markup. Return a yw7 markup string."""
    text = text.replace('<i>', '[i]')
    text = text.replace('<I>', '[i]')
    text = text.replace('</i>', '[/i]')
    text = text.replace('</I>', '[/i]')
    text = text.replace('</em>', '[/i]')
    text = text.replace('</EM>', '[/i]')
    text = text.replace('<b>', '[b]')
    text = text.replace('<B>', '[b]')
    text = text.replace('</b>', '[/b]')
    text = text.replace('</B>', '[/b]')
    text = text.replace('</strong>', '[/b]')
    text = text.replace('</STRONG>', '[/b]')
    text = text.replace('\n', ' ')
    text = text.replace('\r', ' ')
    text = text.replace('\t', ' ')

    text = re.sub('<em.*?>', '[i]', text)
    text = re.sub('<EM.*?>', '[i]', text)
    text = re.sub('<strong.*?>', '[b]', text)
    text = re.sub('<STRONG.*?>', '[b]', text)

    text = text.replace('[/b][b]', '')
    text = text.replace('[/i][i]', '')

    while '  ' in text:
        text = text.replace('  ', ' ')

    return text


def to_html(text):
    """Convert yw7 raw markup to html. Return a html string."""
    try:
        text = text.replace('\n', '</p>\n<p class="firstlineindent">')
        text = text.replace('[i]', '<em>')
        text = text.replace('[/i]', '</em>')
        text = text.replace('[b]', '<strong>')
        text = text.replace('[/b]', '</strong>')
        text = re.sub('\<p(.*?)\> *\<\/p\>', '<p\g<1>><br>\n</p>', text)

    except:
        pass

    return text


def strip_markup(text):
    """Strip yw7 raw markup. Return a plain text string."""
    try:
        text = text.replace('[i]', '')
        text = text.replace('[/i]', '')
        text = text.replace('[b]', '')
        text = text.replace('[/b]', '')

    except:
        pass

    return text


def read_html_file(filePath):
    """Open a html file being encoded utf-8 or ANSI.
    Return a tuple:
    [0] = Message beginning with SUCCESS or ERROR.
    [1] = The file content in a single string. 
    """
    try:
        with open(filePath, 'r', encoding='utf-8') as f:
            text = (f.read())
    except:
        # HTML files exported by a word processor may be ANSI encoded.
        try:
            with open(filePath, 'r') as f:
                text = (f.read())

        except(FileNotFoundError):
            return ('ERROR: "' + filePath + '" not found.', None)

    return ('SUCCESS', text)



HTML_HEADING_MARKERS = ("h2", "h1")
# Index is yWriter's chapter chLevel:
# 0 is for an ordinary chapter
# 1 is for a chapter beginning a section


class HtmlProof(Novel, HTMLParser):
    """HTML file representation of an yWriter project's OfficeFile part.

    Represents a html file with visible chapter and scene tags 
    to be read and written by Open/LibreOffice Writer.
    """

    _FILE_EXTENSION = 'html'
    # overwrites Novel._FILE_EXTENSION

    def __init__(self, filePath):
        Novel.__init__(self, filePath)
        HTMLParser.__init__(self)
        self._lines = []
        self._collectText = False

    def handle_starttag(self, tag, attrs):
        """Recognize the paragraph's beginning.
        Overwrites HTMLparser.handle_endtag().
        """
        if tag == 'p':
            self._collectText = True

    def handle_endtag(self, tag):
        """Recognize the paragraph's end.
        Overwrites HTMLparser.handle_endtag().
        """
        if tag == 'p':
            self._collectText = False

    def handle_data(self, data):
        """Copy the scene paragraphs.
        Overwrites HTMLparser.handle_data().
        """
        if self._collectText:
            self._lines.append(data)

    def read(self):
        """Read scene content from a html file  
        with visible chapter and scene tags.
        Return a message beginning with SUCCESS or ERROR.
        """
        try:
            with open(self._filePath, 'r', encoding='utf-8') as f:
                text = (f.read())
        except:
            # HTML files exported by a word processor may be ANSI encoded.
            try:
                with open(self._filePath, 'r') as f:
                    text = (f.read())

            except(FileNotFoundError):
                return '\nERROR: "' + self._filePath + '" not found.'

        text = to_yw7(text)

        # Invoke HTML parser to write the html body as raw text
        # to self._lines.

        self.feed(text)

        # Parse the HTML body to identify chapters and scenes.

        sceneText = []
        scId = ''
        chId = ''
        inScene = False

        for line in self._lines:

            if line.startswith('[ScID'):
                scId = re.search('[0-9]+', line).group()
                self.scenes[scId] = Scene()
                self.chapters[chId].srtScenes.append(scId)
                inScene = True

            elif line.startswith('[/ScID'):
                self.scenes[scId].sceneContent = '\n'.join(sceneText)
                sceneText = []
                inScene = False

            elif line.startswith('[ChID'):
                chId = re.search('[0-9]+', line).group()
                self.chapters[chId] = Chapter()
                self.srtChapters.append(chId)

            elif line.startswith('[/ChID'):
                pass

            elif inScene:
                sceneText.append(line)

        return 'SUCCESS: ' + str(len(self.scenes)) + ' Scenes read from "' + self._filePath + '".'

    def write(self, novel):
        """Generate a html file containing:
        - chapter ID tags,
        - chapter headings,
        - scene ID tags, 
        - scene content.
        Return a message beginning with SUCCESS or ERROR.
        """

        def format_chapter_title(text):
            """Fix auto-chapter titles for non-English """
            text = text.replace('Chapter ', '')
            return text

        # Copy the novel's attributes to write

        if novel.title is not None:

            if novel.title is not None:
                self.title = novel.title

        if novel.srtChapters != []:
            self.srtChapters = novel.srtChapters

        self.scenes = novel.scenes
        self.chapters = novel.chapters
        lines = [HTML_HEADER.replace('$bookTitle$', self.title)]

        for chId in self.srtChapters:

            if self.chapters[chId].isUnused:
                lines.append(
                    '<p style="font-size:x-small">[ChID:' + chId + ' (Unused)]</p>')

            else:
                lines.append(
                    '<p style="font-size:x-small">[ChID:' + chId + ']</p>')

            headingMarker = HTML_HEADING_MARKERS[self.chapters[chId].chLevel]
            lines.append('<' + headingMarker + '>' + format_chapter_title(
                self.chapters[chId].title) + '</' + headingMarker + '>')

            for scId in self.chapters[chId].srtScenes:
                lines.append('<h4>' + HTML_SCENE_DIVIDER + '</h4>')

                if self.scenes[scId].isUnused:
                    lines.append(
                        '<p style="font-size:x-small">[ScID:' + scId + ' (Unused)]</p>')

                else:
                    lines.append(
                        '<p style="font-size:x-small">[ScID:' + scId + ']</p>')

                if self.scenes[scId].sceneContent is not None:
                    lines.append('<p class="textbody">' +
                                 to_html(self.scenes[scId].sceneContent) + '</p>')

                if self.scenes[scId].isUnused:
                    lines.append(
                        '<p style="font-size:x-small">[/ScID (Unused)]</p>')

                else:
                    lines.append('<p style="font-size:x-small">[/ScID]</p>')

            if self.chapters[chId].isUnused:
                lines.append(
                    '<p style="font-size:x-small">[/ChID (Unused)]</p>')

            else:
                lines.append('<p style="font-size:x-small">[/ChID]</p>')

        lines.append(HTML_FOOTER)
        text = '\n'.join(lines)

        # Remove scene dividers from chapter's beginning

        text = text.replace(
            '</h1>\n<h4>' + HTML_SCENE_DIVIDER + '</h4>', '</h1>')
        text = text.replace(
            '</h2>\n<h4>' + HTML_SCENE_DIVIDER + '</h4>', '</h2>')

        try:
            with open(self._filePath, 'w', encoding='utf-8') as f:
                f.write(text)

        except(PermissionError):
            return 'ERROR: ' + self._filePath + '" is write protected.'

        return 'SUCCESS: "' + self._filePath + '" saved.'

from tkinter import *
from tkinter import messagebox


import xml.etree.ElementTree as ET



def indent(elem, level=0):
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
            indent(elem, level + 1)

        if not elem.tail or not elem.tail.strip():
            elem.tail = i

    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def cdata(filePath, cdataTags: list):
    '''Postprocess the xml file created by ElementTree:
       Put a header on top and insert the missing CDATA tags.
    '''
    with open(filePath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    newlines = ['<?xml version="1.0" encoding="utf-8"?>\n']

    for line in lines:

        for tag in cdataTags:
            line = re.sub('\<' + tag + '\>', '<' +
                          tag + '><![CDATA[', line)
            line = re.sub('\<\/' + tag + '\>',
                          ']]></' + tag + '>', line)

        newlines.append(line)

    newXml = ''.join(newlines)
    newXml = newXml.replace('[CDATA[ \n', '[CDATA[')
    newXml = newXml.replace('\n]]', ']]')

    try:
        with open(filePath, 'w', encoding='utf-8') as f:
            f.write(newXml)

    except:
        return 'ERROR: Can not write"' + filePath + '".'

    return 'SUCCESS: "' + filePath + '" written.'




class Yw7File(Novel):
    """yWriter 7 xml project file representation."""

    _FILE_EXTENSION = '.yw7'
    # overwrites PywFile._FILE_EXTENSION

    def __init__(self, filePath):
        Novel.__init__(self, filePath)
        self._cdataTags = ['Title', 'AuthorName', 'Bio', 'Desc', 'FieldTitle1', 'FieldTitle2', 'FieldTitle3', 'FieldTitle4',
                           'LaTeXHeaderFile', 'Tags', 'AKA', 'ImageFile', 'FullName', 'Goals', 'Notes', 'RTFFile', 'SceneContent']
        # Names of yw7 xml elements containing CDATA.
        # ElementTree.write omits CDATA tags, so they have to be inserted
        # afterwards.

    def read(self):
        """Parse the yw7 xml file located at filePath, fetching the Novel attributes.
        Return a message beginning with SUCCESS or ERROR.
        """

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
            self._tree = ET.parse(self._filePath)
            root = self._tree.getroot()

        except:
            return 'ERROR: Can not process "' + self._filePath + '".'

        prj = root.find('PROJECT')
        self.title = prj.find('Title').text

        if prj.find('AuthorName') is not None:
            self.author = prj.find('AuthorName').text

        if prj.find('Desc') is not None:
            self.summary = prj.find('Desc').text

        self.fieldTitle1 = prj.find('FieldTitle1').text
        self.fieldTitle2 = prj.find('FieldTitle2').text
        self.fieldTitle3 = prj.find('FieldTitle3').text
        self.fieldTitle4 = prj.find('FieldTitle4').text

        for chp in root.iter('CHAPTER'):
            chId = chp.find('ID').text
            self.chapters[chId] = Chapter()
            self.chapters[chId].title = chp.find('Title').text
            self.srtChapters.append(chId)

            if chp.find('Desc') is not None:
                self.chapters[chId].summary = chp.find('Desc').text

            if chp.find('SectionStart') is not None:
                self.chapters[chId].chLevel = 1

            else:
                self.chapters[chId].chLevel = 0

            if chp.find('Unused') is not None:
                self.chapters[chId].isUnused = True

            else:
                self.chapters[chId].isUnused = False

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
                self.scenes[scId].summary = scn.find('Desc').text

            if scn.find('Notes') is not None:
                self.scenes[scId].sceneNotes = scn.find('Notes').text

            if scn.find('Field1') is not None:
                self.scenes[scId].field1 = scn.find('Field1').text

            if scn.find('Field2') is not None:
                self.scenes[scId].field2 = scn.find('Field2').text

            if scn.find('Field3') is not None:
                self.scenes[scId].field3 = scn.find('Field3').text

            if scn.find('Field4') is not None:
                self.scenes[scId].field4 = scn.find('Field4').text

            if scn.find('Tags') is not None:

                if scn.find('Tags').text is not None:
                    self.scenes[scId].tags = scn.find('Tags').text.split(';')

            if scn.find('Unused') is not None:
                self.scenes[scId].isUnused = True

            sceneContent = scn.find('SceneContent').text

            if sceneContent is not None:
                self.scenes[scId].sceneContent = sceneContent

        return 'SUCCESS: ' + str(len(self.scenes)) + ' Scenes read from "' + self._filePath + '".'

    def write(self, novel):
        """Open the yw7 xml file located at filePath and replace a set 
        of items by the novel attributes not being None.
        Return a message beginning with SUCCESS or ERROR.
        """

        # Copy the novel's attributes to write

        if novel.title is not None:
            self.title = novel.title

        if novel.summary is not None:
            self.summary = novel.summary

        if novel.author is not None:
            self.author = novel.author

        if novel.fieldTitle1 is not None:
            self.fieldTitle1 = novel.fieldTitle1

        if novel.fieldTitle2 is not None:
            self.fieldTitle2 = novel.fieldTitle2

        if novel.fieldTitle3 is not None:
            self.fieldTitle3 = novel.fieldTitle3

        if novel.fieldTitle4 is not None:
            self.fieldTitle4 = novel.fieldTitle4

        '''Do not modify these items yet:
        if novel.srtChapters != []:
            self.srtChapters = novel.srtChapters
        '''

        sceneCount = 0

        if novel.scenes != {}:

            for scId in novel.scenes:

                if novel.scenes[scId].title is not None:
                    self.scenes[scId].title = novel.scenes[scId].title

                if novel.scenes[scId].summary is not None:
                    self.scenes[scId].summary = novel.scenes[scId].summary

                if novel.scenes[scId].sceneContent is not None:
                    self.scenes[scId].sceneContent = novel.scenes[scId].sceneContent
                    sceneCount += 1

                if novel.scenes[scId].sceneNotes is not None:
                    self.scenes[scId].sceneNotes = novel.scenes[scId].sceneNotes

                if novel.scenes[scId].field1 is not None:
                    self.scenes[scId].field1 = novel.scenes[scId].field1

                if novel.scenes[scId].field2 is not None:
                    self.scenes[scId].field2 = novel.scenes[scId].field2

                if novel.scenes[scId].field3 is not None:
                    self.scenes[scId].field3 = novel.scenes[scId].field3

                if novel.scenes[scId].field4 is not None:
                    self.scenes[scId].field4 = novel.scenes[scId].field4

                if novel.scenes[scId].tags is not None:
                    self.scenes[scId].tags = novel.scenes[scId].tags

                '''Do not modify these items yet:
                if novel.scenes[scId].isUnused is not None:
                    self.scenes[scId].isUnused = novel.chapters[chId].isUnused
                '''

        if novel.chapters != {}:

            for chId in novel.chapters:

                if novel.chapters[chId].title is not None:
                    self.chapters[chId].title = novel.chapters[chId].title

                if novel.chapters[chId].summary is not None:
                    self.chapters[chId].summary = novel.chapters[chId].summary

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

        root = self._tree.getroot()
        prj = root.find('PROJECT')
        prj.find('Title').text = self.title
        prj.find('FieldTitle1').text = self.fieldTitle1
        prj.find('FieldTitle2').text = self.fieldTitle2
        prj.find('FieldTitle3').text = self.fieldTitle3
        prj.find('FieldTitle4').text = self.fieldTitle4

        if self.summary is not None:

            if prj.find('Desc') is None:
                newDesc = ET.SubElement(prj, 'Desc')
                newDesc.text = self.summary

            else:
                prj.find('Desc').text = self.summary

        if self.author is not None:

            if prj.find('AuthorName') is None:
                newAuth = ET.SubElement(prj, 'AuthorName')
                newAuth.text = self.author

            else:
                prj.find('AuthorName').text = self.author

        for chp in root.iter('CHAPTER'):
            chId = chp.find('ID').text

            if chId in self.chapters:
                chp.find('Title').text = self.chapters[chId].title

                if self.chapters[chId].summary is not None:

                    if chp.find('Desc') is None:
                        newDesc = ET.SubElement(chp, 'Desc')
                        newDesc.text = self.chapters[chId].summary

                    else:
                        chp.find('Desc').text = self.chapters[chId].summary

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

                if self.scenes[scId].title is not None:
                    scn.find('Title').text = self.scenes[scId].title

                if self.scenes[scId].summary is not None:

                    if scn.find('Desc') is None:
                        newDesc = ET.SubElement(scn, 'Desc')
                        newDesc.text = self.scenes[scId].summary

                    else:
                        scn.find('Desc').text = self.scenes[scId].summary

                if self.scenes[scId]._sceneContent is not None:
                    scn.find(
                        'SceneContent').text = self.scenes[scId]._sceneContent
                    scn.find('WordCount').text = str(
                        self.scenes[scId].wordCount)
                    scn.find('LetterCount').text = str(
                        self.scenes[scId].letterCount)

                if self.scenes[scId].sceneNotes is not None:

                    if scn.find('Notes') is None:
                        newNotes = ET.SubElement(scn, 'Notes')
                        newNotes.text = self.scenes[scId].sceneNotes

                    else:
                        scn.find('Notes').text = self.scenes[scId].sceneNotes

                if self.scenes[scId].field1 is not None:

                    if scn.find('Field1') is None:
                        newField = ET.SubElement(scn, 'Field1')
                        newField.text = self.scenes[scId].field1

                    else:
                        scn.find('Field1').text = self.scenes[scId].field1

                if self.scenes[scId].field2 is not None:

                    if scn.find('Field2') is None:
                        newField = ET.SubElement(scn, 'Field2')
                        newField.text = self.scenes[scId].field2

                    else:
                        scn.find('Field2').text = self.scenes[scId].field2

                if self.scenes[scId].field3 is not None:

                    if scn.find('Field3') is None:
                        newField = ET.SubElement(scn, 'Field3')
                        newField.text = self.scenes[scId].field3

                    else:
                        scn.find('Field3').text = self.scenes[scId].field3

                if self.scenes[scId].field4 is not None:

                    if scn.find('Field4') is None:
                        newField = ET.SubElement(scn, 'Field4')
                        newField.text = self.scenes[scId].field4

                    else:
                        scn.find('Field4').text = self.scenes[scId].field4

                if self.scenes[scId].tags is not None:

                    if scn.find('Tags') is None:
                        newTags = ET.SubElement(scn, 'Tags')
                        newTags.text = ';'.join(self.scenes[scId].tags)

                    else:
                        scn.find('Tags').text = ';'.join(
                            self.scenes[scId].tags)

                '''Do not modify these items yet:
                unusedMarker = scn.find('Unused')
                
                if unused is not None:
                    
                    if not self.scenes[scId].isUnused:
                         scn.remove(unusedMarker)
                '''

        indent(root)
        tree = ET.ElementTree(root)

        try:
            self._tree.write(self._filePath, encoding='utf-8')

        except(PermissionError):
            return 'ERROR: "' + self._filePath + '" is write protected.'

        # Postprocess the xml file created by ElementTree
        message = cdata(self._filePath, self._cdataTags)

        if message.startswith('ERROR'):
            return message

        if sceneCount > 0:
            info = str(sceneCount) + ' Scenes'

        else:
            info = 'project data'

        return 'SUCCESS: ' + info + ' written to "' + self._filePath + '".'

    def is_locked(self):
        """Test whether a .lock file placed by yWriter exists.
        """
        if os.path.isfile(self._filePath + '.lock'):
            return True

        else:
            return False


class Yw7Cnv():
    """Converter for yWriter 7 project files.

    # Methods

    yw7_to_document : str
        Arguments
            yw7File : Yw7File
                an object representing the source file.
            documentFile : Novel
                a Novel subclass instance representing the target file.
        Read .yw7 file, parse xml and create a document file.
        Return a message beginning with SUCCESS or ERROR.    

    document_to_yw7 : str
        Arguments
            documentFile : Novel
                a Novel subclass instance representing the source file.
            yw7File : Yw7File
                an object representing the target file.
        Read document file, convert its content to xml, and replace .yw7 file.
        Return a message beginning with SUCCESS or ERROR.

    confirm_overwrite : bool
        Arguments
            fileName : str
                Path to the file to be overwritten
        Ask for permission to overwrite the target file.
        Returns True by default.
        This method is to be overwritten by subclasses with an user interface.
    """

    def yw7_to_document(self, yw7File: Yw7File, documentFile):
        """Read .yw7 file and convert xml to a document file."""
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

    def document_to_yw7(self, documentFile, yw7File):
        """Read document file, convert its content to xml, and replace .yw7 file."""
        if yw7File.is_locked():
            return 'ERROR: yWriter 7 seems to be open. Please close first.'

        if yw7File.filePath is None:
            return 'ERROR: "' + yw7File.filePath + '" is not an yWriter 7 project.'

        if not yw7File.file_exists():
            return 'ERROR: Project "' + yw7File.filePath + '" not found.'

        if not self.confirm_overwrite(yw7File.filePath):
            return 'Program abort by user.'

        if documentFile.filePath is None:
            return 'ERROR: "' + documentFile.filePath + '" is not of the supported type.'

        if not documentFile.file_exists():
            return 'ERROR: "' + documentFile.filePath + '" not found.'

        message = documentFile.read()

        if message.startswith('ERROR'):
            return message

        message = yw7File.read()
        # initialize yw7File data

        if message.startswith('ERROR'):
            return message

        prjStructure = documentFile.get_structure()

        if prjStructure is not None:

            if prjStructure == '':
                return 'ERROR: Source file contains no yWriter project structure information.'

            if prjStructure != yw7File.get_structure():
                return 'ERROR: Structure mismatch - yWriter project not modified.'

        return yw7File.write(documentFile)

    def confirm_overwrite(self, fileName):
        """To be overwritten by subclasses with UI."""
        return True


TITLE = 'PyWriter v1.2'


class CnvRunner(Yw7Cnv):
    """Standalone yWriter 7 converter with a simple GUI. 

    # Arguments

        sourcePath : str
            a full or relative path to the file to be converted.
            Either an .yw7 file or a file of any supported type. 
            The file type determines the conversion's direction.    

        document : Novel
            instance of any Novel subclass representing the 
            source or target document. 

        extension : str
            File extension determining the source or target 
            document's file type. The extension is needed because 
            there can be ambiguous Novel subclasses 
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
            Optional file name suffix used for ambiguous html files.
            Examples:
            - _manuscript for a html file containing scene contents.
            - _scenes for a html file containing scene summaries.
            - _chapters for a html file containing chapter summaries.
    """

    def __init__(self, sourcePath,
                 document,
                 extension,
                 silentMode = True,
                 suffix = ''):
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

    def __run(self, sourcePath,
              document,
              extension,
              suffix):
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

    def confirm_overwrite(self, filePath):
        """ Invoked by the parent if a file already exists. """

        if self.silentMode:
            return True

        else:
            return messagebox.askyesno('WARNING', 'Overwrite existing file "' + filePath + '"?')


def run(sourcePath, silentMode=True):
    document = HtmlProof('')
    converter = CnvRunner(sourcePath, document, 'html', silentMode, '_proof')


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]
    except:
        sourcePath = ''
    run(sourcePath, False)
