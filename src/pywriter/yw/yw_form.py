"""Support yWriter XML formatting.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import re
from html import unescape


def indent_xml(elem, level=0):
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
            indent_xml(elem, level + 1)

        if not elem.tail or not elem.tail.strip():
            elem.tail = i

    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def format_xml(text):
    '''Postprocess the xml file created by ElementTree:
       Insert the missing CDATA tags,
       and replace xml entities by plain text.
    '''

    cdataTags = ['Title', 'AuthorName', 'Bio', 'Desc',
                 'FieldTitle1', 'FieldTitle2', 'FieldTitle3',
                 'FieldTitle4', 'LaTeXHeaderFile', 'Tags',
                 'AKA', 'ImageFile', 'FullName', 'Goals',
                 'Notes', 'RTFFile', 'SceneContent',
                 'Outcome', 'Goal', 'Conflict']
    # Names of yWriter xml elements containing CDATA.
    # ElementTree.write omits CDATA tags, so they have to be inserted
    # afterwards.

    lines = text.split('\n')
    newlines = []

    for line in lines:

        for tag in cdataTags:
            line = re.sub('\<' + tag + '\>', '<' +
                          tag + '><![CDATA[', line)
            line = re.sub('\<\/' + tag + '\>',
                          ']]></' + tag + '>', line)

        newlines.append(line)

    text = '\n'.join(newlines)
    text = text.replace('[CDATA[ \n', '[CDATA[')
    text = text.replace('\n]]', ']]')
    text = unescape(text)

    return text


if __name__ == '__main__':
    pass
