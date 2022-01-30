"""Provide a facade class for a command line user interface.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.pywriter_globals import ERROR
from pywriter.ui.ui import Ui


class UiCmd(Ui):
    """Ui subclass implementing a console interface."""

    def __init__(self, title):
        """Extend the Ui constructor. """
        super().__init__(title)
        print(title)

    def ask_yes_no(self, text):
        result = input(f'WARNING: {text} (y/n)')

        if result.lower() == 'y':
            return True

        else:
            return False

    def set_info_what(self, message):
        """What's the converter going to do?"""
        print(message)

    def set_info_how(self, message):
        """How's the converter doing?"""

        if message.startswith(ERROR):
            message = f'FAIL: {message.split(ERROR, maxsplit=1)[1].strip()}'

        self.infoHowText = message
        print(message)
