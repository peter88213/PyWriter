"""Provide global variables to be imported.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import gettext
import locale
from pathlib import Path

# Initialize localization.
HOME_PATH = str(Path.home()).replace('\\', '/')
LOCALE_PATH = f'{HOME_PATH}/.pywriter/locale/'
CURRENT_LOCALE = locale.getdefaultlocale()[0]
try:
    t = gettext.translation('pywriter', LOCALE_PATH, languages=[CURRENT_LOCALE])
    _ = t.gettext
except:

    def _(message):
        return message

ERROR = '!'
MSG_FILE_WRITTEN = _('File written')
MSG_CANNOT_WRITE_FILE = _('Cannot write file')
MSG_CANNOT_CREATE_FILE = _('Cannot create file')
MSG_CANNOT_CREATE_DIR = _('Cannot create directory')
MSG_CANNOT_OVERWRITE = _('Cannot overwrite file')
MSG_WRITE_PROTECTED = _('File is write protected')
MSG_YWRITER_OPEN = _('yWriter seems to be open. Please close first')
MSG_CANNOT_PROCESS = _('Can not process file')
MSG_FILE_NOT_FOUND = _('File not found')
MSG_ALREADY_EXISTS = _('File already exists')
MSG_WRITE_NOT_BACK = _('This document is not meant to be written back')
MSG_UNSUPPORTED_TYPE = _('File type is not supported')
MSG_UNSUPPORTED_TARGET = _('Target is not of the supported type')
MSG_USER_CANCEL = _('Action canceled by user')
MSG_UNSUPPORTED_EXPORT = _('Export type is not supported')
MSG_NO_PROJECT = _('No yWriter project to write')
MSG_WRONG_CSV_STRUCTURE = _('Wrong csv structure')
MSG_CANNOT_PARSE = _('Cannot parse File')

del _
