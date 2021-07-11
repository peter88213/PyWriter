"""Provide a Configuration class.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
from configparser import ConfigParser


class Configuration():
    """Read/write the program configuration.
    """

    def __init__(self, defaultConfiguration):
        """Define attribute variables.
        defaultSettings - dict of dictionaries
        {category:{option:setting}}
        """
        self.defaultConfiguration = defaultConfiguration
        self.configuration = defaultConfiguration

    def read(self, iniFile):
        """Load the configuration from iniFile.
        Return True, if successful. Otherwise return False.
        """
        config = ConfigParser()

        try:
            config.read(iniFile)

            for cat in self.defaultConfiguration:

                for opt in self.defaultConfiguration[cat]:

                    try:
                        self.configuration[cat][opt] = config.get(cat, opt)

                    except:
                        pass

        except:
            return False

        return True

    def write(self, iniFile):
        """Save the configuration to iniFile.
        Return True, if successful. Otherwise return False.
        """
        config = ConfigParser()

        iniDir = os.path.dirname(iniFile)

        if not os.path.isdir(iniDir):
            os.makedirs(iniDir)

        try:
            for cat in self.defaultConfiguration:
                config.add_section(cat)

                for opt in self.defaultConfiguration[cat]:
                    config.set(cat, opt, self.configuration[cat][opt])

            with open(iniFile, 'w') as f:
                config.write(f)

        except:
            return False

        return True
