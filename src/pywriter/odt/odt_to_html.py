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
        self._heading = None
        self._paragraph = False
        self._comment = None

    def startElement(self, name, attrs):
        """Overrides the xml.sax.ContentHandler method             
        """
        xmlAttributes = {}
        for attribute in attrs.items():
            attrKey, attrValue = attribute
            xmlAttributes[attrKey] = attrValue
        if name == 'text:p':
            if self._comment is not None:
                self._comment += 1
            else:
                self._lines.append('<p>')
                self._paragraph = True
        elif name == 'text:section':
            sectionId = xmlAttributes['text:name']
            self._lines.append(f"<div id='{sectionId}'>\n")
        elif name == 'office:annotation':
            self._lines.append('<!-- ')
            self._comment = 0
        elif name == 'text:h':
            self._heading = f'h{xmlAttributes["text:outline-level"]}'
            self._lines.append(f'<{self._heading}>')
        elif name == 'office:body':
            self._lines.append('<body>\n')
        elif name == 'office:document-content':
            self._lines.append(self._HTML_HEADER)

    def endElement(self, name):
        """Overrides the xml.sax.ContentHandler method     
        """
        if name == 'text:p':
            if self._comment is None:
                self._lines.append('</p>\n')
                self._paragraph = False
        elif name == 'text:section':
            self._lines.append(f"</div>\n")
        elif name == 'office:annotation':
            self._lines.append(' -->')
            self._comment = None
        elif name == 'text:h':
            self._lines.append(f'</{self._heading}>\n')
            self._heading = None
        elif name == 'office:body':
            self._lines.append('</body>')
        elif name == 'office:document-content':
            self._lines.append('</html>\n')

    def characters(self, content):
        """Overrides the xml.sax.ContentHandler method             
        """
        if self._comment is not None:
            if self._comment == 1:
                self._lines.append(content)
        elif self._paragraph:
            self._lines.append(content)
        elif self._heading is not None:
            self._lines.append(content)

    def read(self, filePath):
        """Unpack content.xml and convert its contents to HTML.
        
        Positional arguments:
            filePath -- str: Path of the ODT file. 
        """
        self.filePath = filePath
        try:
            with zipfile.ZipFile(self.filePath, 'r') as odfFile:
                content = odfFile.read('content.xml')
        except ValueError:
            raise Error(f'{_("Cannot read file")}: "{norm_path(self.filePath)}".')

        self._lines = []
        sax.parseString(content, self)
        return ''.join(self._lines)


def main(filePath):
    htmlText = OdtToHtml().read(filePath)
    with open(f'{os.path.splitext(filePath)[0]}.html', 'w', encoding='utf-8') as f:
        f.write(htmlText)


if __name__ == '__main__':
    main(sys.argv[1])

