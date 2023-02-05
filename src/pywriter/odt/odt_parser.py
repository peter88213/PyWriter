"""Provide a class for parsing ODT documents.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import zipfile
from xml import sax
import xml.etree.ElementTree as ET
from pywriter.pywriter_globals import *


class OdtParser(sax.ContentHandler):
    """An ODT document parser, emulating the html.parser.HTMLParser API.
    
    Public methods:
        feed_file(filePath) -- Feed an ODT file to the parser.
    
      HTMLParser compatible API
        handle_starttag -- Stub for a start tag handler to be implemented in a subclass.
        handle_endtag -- Stub for an end tag handler to be implemented in a subclass.
        handle_data -- Stub for a data handler to be implemented in a subclass.
        handle_comment -- Stub for a comment handler to be implemented in a subclass.
        
      Methods overriding xml.sax.ContentHandler methods (not meant to be overridden by subclasses)
        startElement -- Signals the start of an element in non-namespace mode.
        endElement -- Signals the end of an element in non-namespace mode.
        characters -- Receive notification of character data.
    
    The data is presented as from an Open/LibreOffice HTML export file.
    The PyWriter HTML import classes thus can be reused.
    """

    def __init__(self):
        super().__init__()
        self._emTags = ['Emphasis']
        self._strongTags = ['Strong_20_Emphasis']
        self._languageTags = {}
        self._headingTags = {}
        self._heading = None
        self._paragraph = False
        self._commentParagraphCount = None
        self._blockquote = False
        self._list = False
        self._span = []
        self._style = None

    def feed_file(self, filePath):
        """Feed an ODT file to the parser.
        
        Positional arguments:
            filePath -- str: ODT document path.
        
        First unzip the ODT file located at self.filePath, 
        and get languageCode, countryCode, title, desc, and authorName,        
        Then call the sax parser for content.xml.
        """
        try:
            with zipfile.ZipFile(filePath, 'r') as odfFile:
                content = odfFile.read('content.xml')
                meta = odfFile.read('meta.xml')
                styles = odfFile.read('styles.xml')
        except:
            raise Error(f'{_("Cannot read file")}: "{norm_path(filePath)}".')

        #--- Get title, description, and author from 'meta.xml'.
        root = ET.fromstring(meta)
        meta = None
        for element in root.iter():
            if element.tag.endswith('title'):
                if element.text:
                    self.handle_starttag('title', [()])
                    self.handle_data(element.text)
                    self.handle_endtag('title')
            elif element.tag.endswith('description'):
                if element.text:
                    self.handle_starttag('meta', [('', 'description'), ('', element.text)])
            elif element.tag.endswith('initial-creator'):
                if element.text:
                    self.handle_starttag('meta', [('', 'author'), ('', element.text)])

        #--- Get language and country from 'styles.xml'.
        root = ET.fromstring(styles)
        styles = None
        lngCode = None
        ctrCode = None
        for element in root.iter():
            if element.tag.endswith('text-properties'):
                for attribute in element.attrib:
                    if attribute.endswith('language'):
                        lngCode = element.attrib[attribute]
                    elif attribute.endswith('country'):
                        ctrCode = element.attrib[attribute]
            if lngCode and ctrCode:
                if ctrCode != 'none':
                    locale = f'{lngCode}-{ctrCode}'
                else:
                    locale = lngCode
                self.handle_starttag('body', [('lang', locale)])
                break

        root = None

        #--- Parse 'content.xml'.
        sax.parseString(content, self)

    def startElement(self, name, attrs):
        """Signals the start of an element in non-namespace mode.
        
        Overrides the xml.sax.ContentHandler method             
        """
        xmlAttributes = {}
        for attribute in attrs.items():
            attrKey, attrValue = attribute
            xmlAttributes[attrKey] = attrValue
        style = xmlAttributes.get('text:style-name', '')
        if name == 'text:p':
            if self._commentParagraphCount is not None:
                self._commentParagraphCount += 1
            elif style == 'Quotations':
                self.handle_starttag('blockquote', [()])
                self._paragraph = True
                self._blockquote = True
            elif style.startswith('Heading'):
                self._heading = f'h{style[-1]}'
                self.handle_starttag(self._heading, [()])
            elif style in self._headingTags:
                self._heading = self._headingTags[style]
                self.handle_starttag(self._heading, [()])
            elif self._list:
                self.handle_starttag('li', [()])
                self._paragraph = True
            else:
                self.handle_starttag('p', [()])
                self._paragraph = True
        elif name == 'text:span':
            if style in self._emTags:
                self._span.append('em')
                self.handle_starttag('em', [()])
            elif style in self._strongTags:
                self._span.append('strong')
                self.handle_starttag('strong', [()])
            elif style in self._languageTags:
                self._span.append('lang')
                self.handle_starttag('lang', [('lang', self._languageTags[style])])
        elif name == 'text:section':
            sectionId = xmlAttributes['text:name']
            self.handle_starttag('div', [('id', sectionId)])
        elif name == 'office:annotation':
            self._commentParagraphCount = 0
            self._comment = ''
        elif name == 'text:h':
            try:
                self._heading = f'h{xmlAttributes["text:outline-level"]}'
            except:
                self._heading = f'h{style[-1]}'
            self.handle_starttag(self._heading, [()])
        elif name == 'text:list-item':
            self._list = True
        elif name == 'style:style':
            self._style = xmlAttributes.get('style:name', None)
            styleName = xmlAttributes.get('style:parent-style-name', '')
            if styleName.startswith('Heading'):
                self._headingTags[self._style] = f'h{styleName[-1]}'
        elif name == 'style:text-properties':
            if xmlAttributes.get('style:font-style', None) == 'italic':
                self._emTags.append(self._style)
            elif xmlAttributes.get('style:font-weight', None) == 'bold':
                self._strongTags.append(self._style)
            elif xmlAttributes.get('fo:language', False):
                lngCode = xmlAttributes['fo:language']
                ctrCode = xmlAttributes['fo:country']
                if ctrCode != 'none':
                    locale = f'{lngCode}-{ctrCode}'
                else:
                    locale = lngCode
                self._languageTags[self._style] = locale

    def endElement(self, name):
        """Signals the end of an element in non-namespace mode.
        
        Overrides the xml.sax.ContentHandler method     
        """
        if name == 'text:p':
            if self._commentParagraphCount is None:
                if self._blockquote:
                    self.handle_endtag('blockquote')
                    self._blockquote = False
                elif self._heading:
                    self.handle_endtag(self._heading)
                    self._heading = None
                else:
                    self.handle_endtag('p')
                self._paragraph = False
        elif name == 'text:span':
            if self._span:
                self.handle_endtag(self._span.pop())
            print(f'</{self._span}>')
        elif name == 'text:section':
            self.handle_endtag('div')
        elif name == 'office:annotation':
            self.handle_comment(self._comment)
            self._commentParagraphCount = None
        elif name == 'text:h':
            self.handle_endtag(self._heading)
            self._heading = None
        elif name == 'text:list-item':
            self._list = False
        elif name == 'style:style':
            self._style = None

    def characters(self, content):
        """Receive notification of character data.
        
        Overrides the xml.sax.ContentHandler method             
        """
        if self._commentParagraphCount is not None:
            if self._commentParagraphCount == 1:
                self._comment = f'{self._comment}{content}'
        elif self._paragraph:
            self.handle_data(content)
        elif self._heading is not None:
            self.handle_data(content)

    def handle_starttag(self, tag, attrs):
        """Stub for a start tag handler to be implemented in a subclass.
        
        Positional arguments:
            tag -- str: name of the tag converted to lower case.
            attrs -- list of (name, value) pairs containing the attributes found inside the tag’s <> brackets.
        """

    def handle_endtag(self, tag):
        """Stub for an end tag handler to be implemented in a subclass.
        
        Positional arguments:
            tag -- str: name of the tag converted to lower case.
        """

    def handle_data(self, data):
        """Stub for a data handler to be implemented in a subclass.

        Positional arguments:
            data -- str: text to be stored. 
        """

    def handle_comment(self, data):
        """Stub for a comment handler to be implemented in a subclass.
        
        Positional arguments:
            data -- str: comment text. 
        """

