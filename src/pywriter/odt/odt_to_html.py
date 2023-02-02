"""Provide a class for converting ODT content to HTML.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import sys
import zipfile
from xml import sax
from pywriter.pywriter_globals import *


class OdtToHtml(sax.ContentHandler):

    _HTML_HEADER = '''<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
</head>
'''

    def __init__(self):
        super().__init__()
        self._emTags = ['Emphasis']
        self._strongTags = ['Strong_20_Emphasis']
        self._languageTags = {}
        self._heading = None
        self._paragraph = False
        self._comment = None
        self._blockquote = False
        self._em = False
        self._strong = False
        self._lang = False
        self._style = None

    def startElement(self, name, attrs):
        """Overrides the xml.sax.ContentHandler method             
        """
        xmlAttributes = {}
        for attribute in attrs.items():
            attrKey, attrValue = attribute
            xmlAttributes[attrKey] = attrValue
        style = xmlAttributes.get('text:style-name', '')
        if name == 'text:p':
            if self._comment is not None:
                self._comment += 1
            elif style == 'Quotations':
                self.handle_starttag('blockquote', [()])
                self._paragraph = True
                self._blockquote = True
            else:
                self.handle_starttag('p', [()])
                self._paragraph = True
        elif name == 'text:span':
            if style in self._emTags:
                self._em = True
                self.handle_starttag('em', [()])
            elif style in self._strongTags:
                self._strong = True
                self.handle_starttag('strong', [()])
            elif style in self._languageTags:
                self._lang = True
                self.handle_starttag('span', [('lang', self._languageTags[style])])
        elif name == 'text:section':
            sectionId = xmlAttributes['text:name']
            self.handle_starttag('div', [('id', sectionId)])
        elif name == 'office:annotation':
            self._comment = 0
        elif name == 'text:h':
            self._heading = f'h{xmlAttributes["text:outline-level"]}'
            self.handle_starttag(self._heading, [()])
        elif name == 'style:style':
            self._style = xmlAttributes.get('style:name', None)
        elif name == 'style:text-properties':
            if xmlAttributes.get('style:font-style-complex', None) == 'italic':
                self._emTags.append(self._style)
            elif xmlAttributes.get('style:font-weight-complex', None) == 'bold':
                self._strongTags.append(self._style)
            elif xmlAttributes.get('style:language-complex', False):
                self._languageTags[self._style] = xmlAttributes['style:language-complex']
            elif xmlAttributes.get('fo:language', False):
                language = xmlAttributes['fo:language']
                country = xmlAttributes['fo:country']
                self._languageTags[self._style] = f'{language}-{country}'

    def endElement(self, name):
        """Overrides the xml.sax.ContentHandler method     
        """
        if name == 'text:p':
            if self._comment is None:
                if self._blockquote:
                    self.handle_endtag('blockquote')
                    self._blockquote = False
                else:
                    self.handle_endtag('p')
                self._paragraph = False
        elif name == 'text:span':
            if self._em:
                self._em = False
                self.handle_endtag('em')
            elif self._strong:
                self._strong = False
                self.handle_endtag('strong')
            elif self._lang:
                self._lang = False
        elif name == 'text:section':
            self.handle_endtag('div')
        elif name == 'office:annotation':
            self._comment = None
        elif name == 'text:h':
            self.handle_endtag(self._heading)
            self._heading = None
        elif name == 'style:style':
            self._style = None

    def characters(self, content):
        """Overrides the xml.sax.ContentHandler method             
        """
        if self._comment is not None:
            if self._comment == 1:
                self.handle_comment(content)
        elif self._paragraph:
            self.handle_data(content)
        elif self._heading is not None:
            self.handle_data(content)

    def handle_starttag(self, tag, attrs):
        """Stub for a start tag handler.
        
        Positional arguments:
            tag -- str: name of the tag converted to lower case.
            attrs -- list of (name, value) pairs containing the attributes found inside the tag’s <> brackets.
        """

    def handle_endtag(self, tag):
        """Stub for an end tag handler.
        
        Positional arguments:
            tag -- str: name of the tag converted to lower case.
        """

    def handle_data(self, data):
        """Stub for a data handler.

        Positional arguments:
            data -- str: text to be stored. 
        """

    def handle_comment(self, data):
        """Stub for a comment handler.
        
        Positional arguments:
            data -- str: comment text. 
        """

    def read(self):
        """Unpack content.xml and convert its contents to HTML.
        """
        try:
            with zipfile.ZipFile(self.filePath, 'r') as odfFile:
                content = odfFile.read('content.xml')
        except:
            raise Error(f'{_("Cannot read file")}: "{norm_path(self.filePath)}".')

        sax.parseString(content, self)


def main(filePath):
    converter = OdtToHtml()
    converter.filePath = filePath
    htmlText = converter.read(filePath)
    with open(f'{os.path.splitext(filePath)[0]}.html', 'w', encoding='utf-8') as f:
        f.write(htmlText)


if __name__ == '__main__':
    main(sys.argv[1])

