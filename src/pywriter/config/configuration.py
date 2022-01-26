"""Provide a Configuration class for reading and writing INI files.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from configparser import ConfigParser


class Configuration():
    """Read/write the program configuration.

        INI file sections:
        <self.sLabel> - Strings
        <self.oLabel> - Boolean values

    Instance variables:    
        settings - dictionary of strings
        options - dictionary of boolean values
    """

    def __init__(self, settings={}, options={}):
        """Define attribute variables.

        Arguments:
        settings - default settings (dictionary of strings)
        options - default options (dictionary of boolean values)
        """
        self.sLabel = 'SETTINGS'
        self.oLabel = 'OPTIONS'
        self.set(settings, options)

    def set(self, settings=None, options=None):
        """Set the entire configuration without writing the INI file.
        """

        if settings is not None:
            self.settings = settings.copy()

        if options is not None:
            self.options = options.copy()

    def read(self, iniFile):
        """Read a configuration file.
        Settings and options that can not be read in, remain unchanged.
        """
        config = ConfigParser()
        config.read(iniFile)

        if config.has_section(self.sLabel):

            section = config[self.sLabel]

            for setting in self.settings:
                fallback = self.settings[setting]
                self.settings[setting] = section.get(setting, fallback)

        if config.has_section(self.oLabel):

            section = config[self.oLabel]

            for option in self.options:
                fallback = self.options[option]
                self.options[option] = section.getboolean(option, fallback)

    def write(self, iniFile):
        """Save the configuration to iniFile.
        """
        config = ConfigParser()

        if self.settings != {}:

            config.add_section(self.sLabel)

            for settingId in self.settings:
                config.set(self.sLabel, settingId, str(self.settings[settingId]))

        if self.options != {}:

            config.add_section(self.oLabel)

            for settingId in self.options:

                if self.options[settingId]:
                    config.set(self.oLabel, settingId, 'Yes')

                else:
                    config.set(self.oLabel, settingId, 'No')

        with open(iniFile, 'w') as f:
            config.write(f)
