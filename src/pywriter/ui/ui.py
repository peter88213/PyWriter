"""Provide a base class for user interface facades.

All UI facades inherit from this class. 

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.pywriter_globals import ERROR

import sys


class Ui():
    """Base class for UI facades, implementing a 'silent mode'.
    """

    def __init__(self, title):
        """Initialize text buffers for messaging.
        """
        self.infoWhatText = ''
        self.infoHowText = ''

    def ask_yes_no(self, text):
        """The application may use a subclass  
        for confirmation requests.    
        """
        return True

    def set_info_what(self, message):
        """What's the converter going to do?"""
        self.infoWhatText = message

    def set_info_how(self, message):
        """How's the converter doing?"""

        if message.startswith(ERROR):
            message = f'FAIL: {message.split(ERROR, maxsplit=1)[1].strip()}'
            sys.stderr.write(message)

        self.infoHowText = message

    def start(self):
        """To be overridden by subclasses requiring
        special action to launch the user interaction.
        """
