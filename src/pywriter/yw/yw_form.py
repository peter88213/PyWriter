"""Support yWriter XML formatting.

Part of the PyWriter project.
Copyright (c) 2020, peter88213
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import re
import html

EM_DASH = '—'
EN_DASH = '–'
SAFE_DASH = '--'


def replace_unsafe_glyphs(text):
    """Replace glyphs being corrupted by yWriter with safe substitutes. """
    return text.replace(EN_DASH, SAFE_DASH).replace(EM_DASH, SAFE_DASH)


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


def xml_postprocess(filePath, fileEncoding, cdataTags: list):
    '''Postprocess the xml file created by ElementTree:
       Put a header on top, insert the missing CDATA tags,
       and replace "ampersand" xml entity by plain text.
    '''
    with open(filePath, 'r', encoding=fileEncoding) as f:
        lines = f.readlines()

    newlines = ['<?xml version="1.0" encoding="' + fileEncoding + '"?>\n']

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
    newXml = newXml.replace('&amp;', '&')
    newXml = html.unescape(newXml)

    try:
        with open(filePath, 'w', encoding=fileEncoding) as f:
            f.write(newXml)

    except:
        return 'ERROR: Can not write"' + filePath + '".'

    return 'SUCCESS: "' + filePath + '" written.'


if __name__ == '__main__':
    pass
