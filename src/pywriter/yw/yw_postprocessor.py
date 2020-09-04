"""Postprocess yWriter project.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import re
from html import unescape
from abc import abstractmethod


class YwPostprocessor():

    @abstractmethod
    def postprocess_xml_file(self, ywFile):
        '''Postprocess the xml file created by ElementTree:
        Put a header on top, insert the missing CDATA tags,
        and replace xml entities by plain text.
        Return a message beginning with SUCCESS or ERROR.
        '''

    def format_xml(self, text):
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
