"""Provide a pygettext substitute.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
VERSION = '0.2'

import os
import sys
import re
from string import Template
from datetime import datetime

msgPatterns = [re.compile('_\(\"(.+?)\"\)'),
              re.compile('_\(\'(.+?)\'\)'),
              ]

potHeader = '''\
# ${app} Dictionary
# Copyright (C) 2022 Peter Triesberger
#
msgid ""
msgstr ""
"POT-Creation-Date: ${datetime}\\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"
"Language: LANGUAGE\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"Generated-By: PyWriter pgettext.py ${version}\\n"

'''


class PotFile:
    """GNU gettext pot file generator.
    
    Recursive source code scanner looking for message strings.
    Escape double quotes in messages.
    This works also for Python 3.6+ f-strings.   
    """

    def __init__(self, filePath='messages.pot', app=''):
        self.filePath = filePath
        self.msgList = []
        self.app = app

    def write_pot(self):
        map = {'app':self.app,
               'datetime':datetime.today().replace(microsecond=0).isoformat(sep=' '),
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


def main(path):
    # Generate a template file (pot) for message translation.
    potFile = '../i18n/messages.pot'
    print(f'Writing "{potFile}" ...')
    if os.path.isfile(potFile):
        os.replace(potFile, f'{potFile}.bak')
        backedUp = True
    else:
        backedUp = False
    try:
        pot = PotFile(potFile)
        pot.scan_dir(path)
        pot.write_pot()
    except:
        if backedUp:
            os.replace(f'{potFile}.bak', potFile)
        print(f'ERROR: Cannot write file: "{potFile}".')


if __name__ == '__main__':
    try:
        path = sys.argv[1]
    except:
        path = '.'
    main(path)
