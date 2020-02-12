"""OdtFile - Class for OpenDocument xml file operations and parsing.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import re
import zipfile
import locale
import xml.etree.ElementTree as ET
from shutil import rmtree

from pywriter.model.novel import Novel
from pywriter.model.chapter import Chapter
from pywriter.model.scene import Scene
from pywriter.model.xform import *
from pywriter.model.odtform import *


class OdtFile(Novel):
    """OpenDocument xml project file representation."""

    _FILE_EXTENSION = '.odt'
    _TEMPDIR = 'odt'
    _TEMPLATE_FILE = 'template.zip'
    _ODT_COMPONENTS = ['Configurations2', 'manifest.rdf', 'META-INF', 'content.xml', 'meta.xml', 'mimetype', 'settings.xml', 'styles.xml', 'Thumbnails', 'Configurations2/accelerator', 'Configurations2/floater', 'Configurations2/images', 'Configurations2/menubar',
                       'Configurations2/popupmenu', 'Configurations2/progressbar', 'Configurations2/statusbar', 'Configurations2/toolbar', 'Configurations2/toolpanel', 'Configurations2/accelerator/current.xml', 'Configurations2/images/Bitmaps', 'META-INF/manifest.xml', 'Thumbnails/thumbnail.png']

    def __init__(self, filePath):
        Novel.__init__(self, filePath)

        self.sections = False
        self.proofread = False
        self.bookmarks = False
        self.comments = False

    def read(self):
        """Parse the odt content.xml file located at filePath, fetching the Novel attributes.
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
        """Generate a html file containing:
        - chapter sections containing:
            - chapter headings,
            - scene sections containing:
                - scene ID as anchor, 
                - scene title as comment,
                - scene content.
        Return a message beginning with SUCCESS or ERROR.
        """

        def setup_odt():
            try:
                rmtree(self._TEMPDIR)

            except:
                pass

            os.mkdir(self._TEMPDIR)

            with zipfile.ZipFile(self._TEMPLATE_FILE, 'r') as odtTemplate:
                odtTemplate.extractall(self._TEMPDIR)

        def format_chapter_title(text):
            """Fix auto-chapter titles for non-English """
            text = text.replace('Chapter ', '')
            return text

        def set_locale():
            localeCodes = locale.getdefaultlocale()[0].split('_')
            languageCode = localeCodes[0]
            countryCode = localeCodes[1]
            try:
                with open(self._TEMPDIR + '/styles.xml', 'r', encoding='utf-8') as f:
                    text = f.read()

            except:
                return 'ERROR: cannot read "styles.xml"'

            text = re.sub('fo\:language\=\"..',
                          'fo:language="' + languageCode, text)
            text = re.sub('fo\:country\=\"..',
                          'fo:country="' + countryCode, text)
            try:
                with open(self._TEMPDIR + '/styles.xml', 'w', encoding='utf-8') as f:
                    f.write(text)

            except:
                return 'ERROR: Cannot write "styles.xml"'

            return 'SUCCESS: Locale set to "' + locale.getdefaultlocale()[0] + '".'

        def write_content():
            lines = [ODT_HEADER]

            for chId in self.srtChapters:

                if self.sections and self.chapters[chId].chType == 0 and not self.chapters[chId].isUnused:
                    lines.append(
                        '<text:section text:style-name="Sect1" text:name="ChID:' + chId + '">')

                if self.proofread:
                    if self.chapters[chId].isUnused:
                        lines.append(
                            '<text:p text:style-name="yWriter_20_mark_20_unused">[ChID:' + chId + ' (Unused)]</text:p>')

                    elif self.chapters[chId].chType != 0:
                        lines.append(
                            '<text:p text:style-name="yWriter_20_mark_20_info">[ChID:' + chId + ' (Info)]</text:p>')

                    else:
                        lines.append(
                            '<text:p text:style-name="yWriter_20_mark">[ChID:' + chId + ']</text:p>')

                if self.proofread or ((not self.chapters[chId].isUnused) and self.chapters[chId].chType == 0):
                    headingMarker = ODT_HEADING_MARKERS[self.chapters[chId].chLevel]
                    lines.append(headingMarker + format_chapter_title(
                        self.chapters[chId].title) + '</text:h>')

                    firstSceneInChapter = True

                    for scId in self.chapters[chId].srtScenes:

                        if self.proofread or not self.scenes[scId].isUnused:

                            if not firstSceneInChapter:
                                lines.append(
                                    '<text:p text:style-name="Heading_20_4">' + SCENE_DIVIDER + '</text:p>')

                            if self.sections:
                                lines.append(
                                    '<text:section text:style-name="Sect1" text:name="ScID:' + scId + '">')

                            if self.proofread:

                                if self.scenes[scId].isUnused or self.chapters[chId].isUnused:
                                    lines.append(
                                        '<text:p text:style-name="yWriter_20_mark_20_unused">[ScID:' + scId + ' (Unused)]</text:p>')

                                elif self.chapters[chId].chType != 0:
                                    lines.append(
                                        '<text:p text:style-name="yWriter_20_mark_20_info">[ScID:' + scId + ' (Info)]</text:p>')

                                else:
                                    lines.append(
                                        '<text:p text:style-name="yWriter_20_mark">[ScID:' + scId + ']</text:p>')

                            scenePrefix = '<text:p text:style-name="Text_20_body">'

                            if self.bookmarks:
                                scenePrefix += '<text:bookmark text:name="ScID:' + scId + '"/>'

                            if self.comments:
                                scenePrefix += ('<office:annotation>\n' +
                                                '<dc:creator>scene title</dc:creator>\n' +
                                                '<text:p>' + self.scenes[scId].title + '</text:p>\n' +
                                                '</office:annotation>')

                            if self.scenes[scId].sceneContent is not None:
                                lines.append(scenePrefix +
                                             to_odt(self.scenes[scId].sceneContent) + '</text:p>')

                            else:
                                lines.append(scenePrefix + '</text:p>')

                            firstSceneInChapter = False

                            if self.proofread:

                                if self.scenes[scId].isUnused or self.chapters[chId].isUnused:
                                    lines.append(
                                        '<text:p text:style-name="yWriter_20_mark_20_unused">[/ScID (Unused)]</text:p>')

                                elif self.chapters[chId].chType != 0:
                                    lines.append(
                                        '<text:p text:style-name="yWriter_20_mark_20_info">[/ScID (Info)]</text:p>')

                                else:
                                    lines.append(
                                        '<text:p text:style-name="yWriter_20_mark">[/ScID]</text:p>')

                            if self.sections:
                                lines.append('</text:section>')

                if self.proofread:

                    if self.chapters[chId].isUnused:
                        lines.append(
                            '<text:p text:style-name="yWriter_20_mark_20_unused">[/ChID (Unused)]</text:p>')

                    elif self.chapters[chId].chType != 0:
                        lines.append(
                            '<text:p text:style-name="yWriter_20_mark_20_info">[/ChID (Info)]</text:p>')

                    else:
                        lines.append(
                            '<text:p text:style-name="yWriter_20_mark">[/ChID]</text:p>')

                if self.sections and self.chapters[chId].chType == 0 and not self.chapters[chId].isUnused:
                    lines.append('</text:section>')

            lines.append(ODT_FOOTER)
            text = '\n'.join(lines)

            try:
                with open(self._TEMPDIR + '/content.xml', 'w', encoding='utf-8') as f:
                    f.write(text)

            except:
                return 'ERROR: Cannot write "content.xml".'

            return 'SUCCESS: Content written to "content.xml"'

        # Copy the novel's attributes to write

        if novel.title is not None:
            if novel.title != '':
                self.title = novel.title

        if novel.srtChapters != []:
            self.srtChapters = novel.srtChapters

        if novel.scenes is not None:
            self.scenes = novel.scenes

        if novel.chapters is not None:
            self.chapters = novel.chapters

        setup_odt()

        message = write_content()

        if message.startswith('ERROR'):
            return message

        message = set_locale()

        if message.startswith('ERROR'):
            return message

        try:
            with zipfile.ZipFile(self.filePath, 'w') as odtTarget:
                workdir = os.getcwd()
                os.chdir(self._TEMPDIR)
                for file in self._ODT_COMPONENTS:
                    odtTarget.write(file)
        except:
            os.chdir(workdir)
            return 'ERROR: Cannot generate "' + self._filePath + '".'

        os.chdir(workdir)

        return 'SUCCESS: "' + self._filePath + '" saved.'
