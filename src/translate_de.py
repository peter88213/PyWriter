"""Generate German translation files for GNU gettext.

- Update the project's 'de.po' translation file.
- Generate the language specific 'pywriter.mo' dictionary.

Usage: 
translate_de.py

File structure:

├── PyWriter/
│   ├── i18n/
│   │   └── de.json
│   └── src/
│       ├── translations.py
│       └── msgfmt.py
└── <project>/
    ├── src/ 
    │   └── translate_de.py
    └── i18n/
        ├── messages.pot
        ├── de.po
        └── locale/
            └─ de/
               └─ LC_MESSAGES/
                  └─ pywriter.mo
    
Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from shutil import copyfile
import translations
import msgfmt

APP_NAME = 'PyWriter'
PO_PATH = '../i18n/de.po'
MO_PATH = '../i18n/locale/de/LC_MESSAGES/pywriter.mo'
MO_COPY = '../src/sample/locale/de/LC_MESSAGES/pywriter.mo'

if translations.main('de', app=APP_NAME):
    print(f'Writing "{MO_PATH}" ...')
    msgfmt.make(PO_PATH, MO_PATH)
    copyfile(MO_PATH, MO_COPY)
