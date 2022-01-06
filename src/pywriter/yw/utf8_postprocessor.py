"""Provide a strategy class to postprocess utf-8 encoded yWriter project files.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import re
from html import unescape


class Utf8Postprocessor():
    """Postprocess utf-8 encoded yWriter project."""

    def __init__(self):
        """Initialize instance variables."""
        self.cdataTags = ['Title', 'AuthorName', 'Bio', 'Desc',
                          'FieldTitle1', 'FieldTitle2', 'FieldTitle3',
                          'FieldTitle4', 'LaTeXHeaderFile', 'Tags',
                          'AKA', 'ImageFile', 'FullName', 'Goals',
                          'Notes', 'RTFFile', 'SceneContent',
                          'Outcome', 'Goal', 'Conflict']
        # Names of yWriter xml elements containing CDATA.
        # ElementTree.write omits CDATA tags, so they have to be inserted
        # afterwards.

    def format_xml(self, text):
        '''Postprocess the xml file created by ElementTree:
           Insert the missing CDATA tags,
           and replace xml entities by plain text.
        '''
        lines = text.split('\n')
        newlines = []

        for line in lines:

            for tag in self.cdataTags:
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

    def postprocess_xml_file(self, filePath):
        '''Postprocess the xml file created by ElementTree:
        Put a header on top, insert the missing CDATA tags,
        and replace xml entities by plain text.
        Return a message beginning with SUCCESS or ERROR.
        '''

        with open(filePath, 'r', encoding='utf-8') as f:
            text = f.read()

        text = self.format_xml(text)
        text = '<?xml version="1.0" encoding="utf-8"?>\n' + text

        try:

            with open(filePath, 'w', encoding='utf-8') as f:
                f.write(text)

        except:
            return 'ERROR: Can not write "' + os.path.normpath(filePath) + '".'

        return 'SUCCESS: "' + os.path.normpath(filePath) + '" written.'
