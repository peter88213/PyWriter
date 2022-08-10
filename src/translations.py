"""Provide a class to handle GNU gettext translation files.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys
import os
import json


class Translations:
    """Class to handle GNU gettext translation files.
    
    .po file and .pot file are in the same directory.   
    """

    def __init__(self, poFile):
        self.poFile = poFile.replace('\\', '/')
        self.lngFile = f'{os.path.splitext(self.poFile)[0]}.json'
        filePath = os.path.dirname(self.poFile)
        if not filePath:
            filePath = '.'
        self.potFile = f'{filePath}/messages.pot'

        self.msgDict = {}
        self.msgList = []
        self.header = ''

    def read_json(self):
        """Read a JSON translation file and add the translations to msgDict."""
        try:
            with open(self.lngFile, 'r', encoding='utf-8') as f:
                print(f'Reading "{self.lngFile}" ...')
                msgDict = json.load(f)
            for message in msgDict:
                self.msgDict[message] = msgDict[message]
            print(f'{len(self.msgDict)} translations')
            return True
        except:
            return False

    def write_json(self):
        """Add translations to a JSON translation file."""
        try:
            with open(self.lngFile, 'w', encoding='utf-8') as f:
                print(f'Writing "{self.lngFile}" ...')
                json.dump(self.msgDict, f, sort_keys=True, indent=2)
                print(f'{len(self.msgDict)} translations')
            return True
        except:
            return False

    def read_pot(self):
        """Read the messages of the '.pot' file.
        
        Parse the file and collect messages in msgList.
        """
        print(f'Reading "{self.potFile}" ...')
        with open(self.potFile, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        inHeader = True
        headerLines = []
        for line in lines:
            line = line.strip()
            if line.startswith('msgid ""'):
                headerLines.append(line)
            elif inHeader:
                if line.startswith('msgid "'):
                    inHeader = False
                    self.header = '\n'.join(headerLines)
                else:
                    headerLines.append(line)
            if not inHeader:
                if line.startswith('msgid "'):
                    self.msgList.append(self._extract_text('msgid "', line))
            self.msgList.sort()

    def read_po(self):
        """Read the existing translations of the '.po' file.
        
        Parse the file and collect translations in msgDict.
        """
        print(f'Reading "{self.poFile}" ...')
        with open(self.poFile, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        inHeader = True
        headerLines = []
        for line in lines:
            line = line.strip()
            if line.startswith('msgid ""'):
                headerLines.append(line)
            elif inHeader:
                if line.startswith('msgid "'):
                    inHeader = False
                    self.header = '\n'.join(headerLines)
                else:
                    headerLines.append(line)
            if not inHeader:
                if line.startswith('msgid "'):
                    message = self._extract_text('msgid "', line)
                elif line.startswith('msgstr "'):
                    translation = self._extract_text('msgstr "', line)
                    self.msgDict[message] = translation
        print(f'{len(self.msgDict)} translations')

    def write_po(self):
        """Write translations to the '.po' file.
        
        Entries are sorted by msgDict key.
        """
        lines = [self.header, '\n', '\n']
        for message in self.msgList:
            try:
                translation = self.msgDict[message]
            except:
                translation = ''
            lines.append(f'msgid "{message}"\nmsgstr "{translation}"\n\n')
        print(f'Writing "{self.poFile}" ...')
        with open(self.poFile, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f'{len(self.msgDict)} translations')

    def _extract_text(self, prefix, line):
        firstPos = len(prefix)
        lastPos = len(line) - 1
        message = line[firstPos:lastPos]
        return message


if __name__ == '__main__':
    fileName = sys.argv[1]
    translations = Translations(fileName)
    translations.read_json()
    translations.read_pot()
    translations.read_po()
    translations.write_po()
    translations.write_json()
