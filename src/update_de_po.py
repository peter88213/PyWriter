"""Update all "de.po" dictionaries from the JSON file.

Use this script only for global changes of existing descriptions.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
from translations import Translations

START_DIR = os.getcwd()
ROOT = '../../'

with os.scandir(ROOT) as prjPaths:
    for prjPath in prjPaths:
        if os.path.isdir(prjPath):
            poFile = f'{prjPath.path}/i18n/de.po'
            if os.path.isfile(poFile):
                print(poFile)
                os.chdir(f'{prjPath.path}/i18n')
                translations = Translations('de')
                translations.read_pot()
                translations.read_po()
                translations.read_json()
                translations.write_po()
os.chdir(START_DIR)
