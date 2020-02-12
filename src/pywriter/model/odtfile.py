"""OdtFile - Class for OpenDocument xml file operations and parsing.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import zipfile
import locale
from shutil import rmtree
from datetime import datetime

from pywriter.model.novel import Novel
from pywriter.model.odtform import *


class OdtFile(Novel):
    """OpenDocument xml project file representation."""

    _FILE_EXTENSION = '.odt'
    _TEMPDIR = 'odt'
    _TEMPLATE_FILE = 'template.zip'
    _ODT_COMPONENTS = ['Configurations2', 'manifest.rdf', 'META-INF', 'content.xml', 'meta.xml', 'mimetype', 'settings.xml', 'styles.xml', 'Configurations2/accelerator', 'Configurations2/floater', 'Configurations2/images', 'Configurations2/menubar',
                       'Configurations2/popupmenu', 'Configurations2/progressbar', 'Configurations2/statusbar', 'Configurations2/toolbar', 'Configurations2/toolpanel', 'Configurations2/accelerator/current.xml', 'Configurations2/images/Bitmaps', 'META-INF/manifest.xml']

    _SCENE_DIVIDER = '* * *'
    # To be placed between scene ending and beginning tags.

    _ODT_HEADER = '''<?xml version="1.0" encoding="UTF-8"?>

<office:document-content xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" xmlns:ooo="http://openoffice.org/2004/office" xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" xmlns:dr3d="urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0" xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0" xmlns:chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0" xmlns:rpt="http://openoffice.org/2005/report" xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0" xmlns:ooow="http://openoffice.org/2004/writer" xmlns:oooc="http://openoffice.org/2004/calc" xmlns:of="urn:oasis:names:tc:opendocument:xmlns:of:1.2" xmlns:css3t="http://www.w3.org/TR/css3-text/" xmlns:tableooo="http://openoffice.org/2009/table" xmlns:calcext="urn:org:documentfoundation:names:experimental:calc:xmlns:calcext:1.0" xmlns:drawooo="http://openoffice.org/2010/draw" xmlns:loext="urn:org:documentfoundation:names:experimental:office:xmlns:loext:1.0" xmlns:grddl="http://www.w3.org/2003/g/data-view#" xmlns:field="urn:openoffice:names:experimental:ooo-ms-interop:xmlns:field:1.0" xmlns:math="http://www.w3.org/1998/Math/MathML" xmlns:form="urn:oasis:names:tc:opendocument:xmlns:form:1.0" xmlns:script="urn:oasis:names:tc:opendocument:xmlns:script:1.0" xmlns:dom="http://www.w3.org/2001/xml-events" xmlns:xforms="http://www.w3.org/2002/xforms" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:formx="urn:openoffice:names:experimental:ooxml-odf-interop:xmlns:form:1.0" xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns:officeooo="http://openoffice.org/2009/office" office:version="1.2">
 <office:scripts/>
 <office:font-face-decls>
  <style:font-face style:name="StarSymbol" svg:font-family="StarSymbol" style:font-charset="x-symbol"/>
 </office:font-face-decls>
 <office:automatic-styles>
  <style:style style:name="Sect1" style:family="section">
   <style:section-properties style:editable="false">
    <style:columns fo:column-count="1" fo:column-gap="0cm"/>
   </style:section-properties>
  </style:style>
 </office:automatic-styles>
 <office:body>
  <office:text text:use-soft-page-breaks="true">
'''

    _ODT_FOOTER = '''  </office:text>
 </office:body>
</office:document-content>
'''

    _ODT_HEADING_MARKERS = ['<text:h text:style-name="Heading_20_2" text:outline-level="2">',
                            '<text:h text:style-name="Heading_20_1" text:outline-level="1">']

    _ODT_META = '''<?xml version="1.0" encoding="utf-8"?>
<office:document-meta xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" xmlns:ooo="http://openoffice.org/2004/office" xmlns:grddl="http://www.w3.org/2003/g/data-view#" office:version="1.2">
  <office:meta>
    <meta:generator>PyWriter</meta:generator>
    <dc:title>%title%</dc:title>
    <dc:description>%summary%</dc:description>
    <dc:subject></dc:subject>
    <meta:keyword></meta:keyword>
    <meta:initial-creator>%author%</meta:initial-creator>
    <dc:creator></dc:creator>
    <meta:creation-date>%date%T%time%Z</meta:creation-date>
    <dc:date></dc:date>
  </office:meta>
</office:document-meta>
'''

    def __init__(self, filePath):
        Novel.__init__(self, filePath)

        self.sections = False
        self.proofread = False
        self.bookmarks = False
        self.comments = False

    def tear_down(self):
        try:
            rmtree(self._TEMPDIR)

        except:
            pass

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

        def set_up():
            self.tear_down()
            os.mkdir(self._TEMPDIR)

            with zipfile.ZipFile(self._TEMPLATE_FILE, 'r') as odtTemplate:
                odtTemplate.extractall(self._TEMPDIR)

        def format_chapter_title(text):
            """Fix auto-chapter titles for non-English """
            text = text.replace('Chapter ', '')
            return text

        def to_odt(text):
            """Convert yw7 raw markup to html. Return a html string."""
            try:
                text = text.replace(
                    '\n', '</text:p>\n<text:p text:style-name="First_20_line_20_indent">')
                text = text.replace(
                    '[i]', '<text:span text:style-name="Emphasis">')
                text = text.replace('[/i]', '</text:span>')
                text = text.replace(
                    '[b]', '<text:span text:style-name="Strong_20_Emphasis">')
                text = text.replace('[/b]', '</text:span>')

            except:
                pass

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

        def write_metadata():
            dt = datetime.today()
            date = str(dt.year) + '-' + str(dt.month).rjust(2, '0') + '-' + \
                str(dt.day).rjust(2, '0')
            time = str(dt.hour).rjust(2, '0') + ':' + \
                str(dt.minute).rjust(2, '0') + ':' + \
                str(dt.second).rjust(2, '0')
            text = self._ODT_META.replace('%author%', self.author).replace('%title%', self.title).replace(
                '%summary%', '<![CDATA[' + self.summary + ']]>').replace('%date%', date).replace('%time%', time)

            try:
                with open(self._TEMPDIR + '/meta.xml', 'w', encoding='utf-8') as f:
                    f.write(text)

            except:
                return 'ERROR: Cannot write "meta.xml".'

            return 'SUCCESS: Metadata written to "meta.xml"'

        def write_content():
            lines = [self._ODT_HEADER]

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
                    headingMarker = self._ODT_HEADING_MARKERS[self.chapters[chId].chLevel]
                    lines.append(headingMarker + format_chapter_title(
                        self.chapters[chId].title) + '</text:h>')

                    firstSceneInChapter = True

                    for scId in self.chapters[chId].srtScenes:

                        if self.proofread or not self.scenes[scId].isUnused:

                            if not firstSceneInChapter:
                                lines.append(
                                    '<text:p text:style-name="Heading_20_4">' + self._SCENE_DIVIDER + '</text:p>')

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

            lines.append(self._ODT_FOOTER)
            text = '\n'.join(lines)

            try:
                with open(self._TEMPDIR + '/content.xml', 'w', encoding='utf-8') as f:
                    f.write(text)

            except:
                return 'ERROR: Cannot write "content.xml".'

            return 'SUCCESS: Content written to "content.xml"'

        # Copy the novel's attributes to write

        if novel.title is None:
            self.title = ''

        else:
            self.title = novel.title

        if novel.summary is None:
            self.summary = ''

        else:
            self.summary = novel.summary

        if novel.author is None:
            self.author = ''

        else:
            self.author = novel.author

        if novel.srtChapters != []:
            self.srtChapters = novel.srtChapters

        if novel.scenes is not None:
            self.scenes = novel.scenes

        if novel.chapters is not None:
            self.chapters = novel.chapters

        set_up()

        message = write_content()

        if message.startswith('ERROR'):
            return message

        message = write_metadata()

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
        self.tear_down()
        return 'SUCCESS: "' + self._filePath + '" saved.'
