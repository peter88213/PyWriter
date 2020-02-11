"""Support HTML conversion and formatting.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import re


SCENE_DIVIDER = '* * *'
# To be placed between scene ending and beginning tags.

ODT_HEADER = '''<?xml version="1.0" encoding="UTF-8"?>

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
   <office:forms form:automatic-focus="false" form:apply-design-mode="false"/>
   <text:sequence-decls>
    <text:sequence-decl text:display-outline-level="0" text:name="Illustration"/>
    <text:sequence-decl text:display-outline-level="0" text:name="Table"/>
    <text:sequence-decl text:display-outline-level="0" text:name="Text"/>
    <text:sequence-decl text:display-outline-level="0" text:name="Drawing"/>
    <text:sequence-decl text:display-outline-level="0" text:name="Figure"/>
   </text:sequence-decls>
'''

ODT_FOOTER = '''  </office:text>
 </office:body>
</office:document-content>
'''

ODT_HEADING_MARKERS = ['<text:h text:style-name="Heading_20_2" text:outline-level="2">',
                       '<text:h text:style-name="Heading_20_1" text:outline-level="1">']
'''
<text:h text:style-name="Heading_20_1" text:outline-level="1"></text:h>
<text:h text:style-name="Heading_20_2" text:outline-level="2"></text:h>
<text:p text:style-name="Heading_20_4"></text:p>
<text:p text:style-name="Text_20_body"></text:p>
<text:p text:style-name="First_20_line_20_indent"></text:p>
'''


def to_yw7(text):
    """Convert html tags to yw7 raw markup. Return a yw7 markup string."""
    text = text.replace('<text:span text:style-name="Emphasis">', '[i]')
    text = text.replace(
        '<text:span text:style-name="Strong_20_Emphasis">', '[b]')
    text = text.replace('</text:span>', '[/i]')
    text = text.replace('\n', ' ')
    text = text.replace('\r', ' ')
    text = text.replace('\t', ' ')

    text = text.replace('[/b][b]', '')
    text = text.replace('[/i][i]', '')

    while '  ' in text:
        text = text.replace('  ', ' ')

    return text


def to_odt(text):
    """Convert yw7 raw markup to html. Return a html string."""
    try:
        text = text.replace(
            '\n', '</text:p>\n<text:p text:style-name="First_20_line_20_indent">')
        text = text.replace('[i]', '<text:span text:style-name="Emphasis">')
        text = text.replace('[/i]', '</text:span>')
        text = text.replace(
            '[b]', '<text:span text:style-name="Strong_20_Emphasis">')
        text = text.replace('[/b]', '</text:span>')

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


def read_xml_file(filePath):
    """Open a xml file being encoded utf-8.
    Return a tuple:
    [0] = Message beginning with SUCCESS or ERROR.
    [1] = The file content in a single string. 
    """
    try:
        with open(filePath, 'r', encoding='utf-8') as f:
            text = (f.read())
    except(FileNotFoundError):
        return ('ERROR: "' + filePath + '" not found.', None)

    return ('SUCCESS', text)


if __name__ == '__main__':
    pass
