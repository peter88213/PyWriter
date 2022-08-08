"""Provide a pygettext substitute.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
VERSION = '0.1'

import os
import sys
import re
from string import Template
from datetime import datetime

msgPatterns = [re.compile('_\(\"(.+?)\"\)'),
              re.compile('_\(\'(.+?)\'\)'),
              ]

potHeader = '''\
# SOME DESCRIPTIVE TITLE.
# Copyright (C) YEAR ORGANIZATION
# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.
#
msgid ""
msgstr ""
"Project-Id-Version: PACKAGE VERSION\\n"
"POT-Creation-Date: ${datetime}\\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"
"Language-Team: LANGUAGE <LL@li.org>\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"Generated-By: PyWriter gettext.py ${version}\\n"

'''


class PotFile:
    """GNU gettext pot file generator.
    
    Recursive source code scanner looking for message strings.
    Escape double quotes in messages.
    This works also for Python 3.6+ f-strings.   
    """

    def __init__(self, filePath='messages.pot'):
        self.filePath = filePath
        self.msgList = []

    def write_pot(self):
        map = {'datetime':datetime.today().replace(microsecond=0).isoformat(sep=' '),
               'version': VERSION,
               }
        hdTemplate = Template(potHeader)
        potText = hdTemplate.safe_substitute(map)
        self.msgList = list(set(self.msgList))
        self.msgList.sort()
        for message in self.msgList:
            message = message.replace('"', '\\"')
            print(message)
            entry = f'\nmsgid "{message}"\nmsgstr ""\n'
            potText += entry
        with open(self.filePath, 'w', encoding='utf-8') as f:
            f.write(potText)
            print(f'\nPot file "{self.filePath}" written.')

    def get_messages(self, text):
        result = []
        for msgPattern in msgPatterns:
            result.extend(msgPattern.findall(text))
        return result

    def scan_file(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()
            print(f'Processing "{filename}"...')
        self.msgList.extend(self.get_messages(text))

    def scan_dir(self, path):
        with os.scandir(path) as it:
            for entry in it:
                if entry.name.endswith('.py') and entry.is_file():
                    file = f'{entry.path}'.replace('\\', '/')
                    self.scan_file(file)
                elif entry.is_dir():
                    self.scan_dir(entry.path)


if __name__ == '__main__':
    try:
        path = sys.argv[1]
    except:
        path = '.'
    pot = PotFile('messages.pot')
    pot.scan_dir(path)
    pot.write_pot()
