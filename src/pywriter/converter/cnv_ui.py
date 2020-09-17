"""User interface for the converter: abstract facade

Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""


class CnvUi():
    """Superclass for UI facades, implementing a 'silent mode'."""

    def __init__(self, title):
        self.infoWhatText = ''
        self.infoHowText = ''

    def ask_yes_no(self, text):
        return True

    def set_info_what(self, message):
        """What's the converter going to do?"""
        self.infoWhatText = message

    def set_info_how(self, message):
        """How's the converter doing?"""
        self.infoHowText = message

    def get_info_how(self):
        return self.infoHowText
