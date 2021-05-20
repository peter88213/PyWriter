"""Provide a facade for a command line user interface.

Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.ui.ui import Ui


class UiCmd(Ui):
    """Ui subclass implementing a console interface."""

    def __init__(self, title):
        """initialize UI. """
        print(title)

    def ask_yes_no(self, text):
        result = input('WARNING: ' + text + ' (y/n)')

        if result.lower() == 'y':
            return True

        else:
            return False

    def set_info_what(self, message):
        """What's the converter going to do?"""
        print(message)

    def set_info_how(self, message):
        """How's the converter doing?"""
        self.infoHowText = message
        print(message)
