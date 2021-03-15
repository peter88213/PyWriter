"""OdfBuilder - Class for OpenDocument xml file generation.

Part of the PyWriter project.
Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import locale
from shutil import rmtree
from datetime import datetime
from string import Template


class OdfBuilder():
    """Abstract class for building an ODF zipfile.
    """

    TEMPDIR = 'temp_odf'

    def tear_down(self):
        """Delete the temporary directory 
        containing the unpacked ODF directory structure.
        """
        try:
            rmtree(self.TEMPDIR)
        except:
            pass

    def set_up(self):
        """Create a temporary directory containing the internal 
        structure of an ODF file except 'content.xml'.
        """
        self.tear_down()
        os.mkdir(self.TEMPDIR)
        os.mkdir(self.TEMPDIR + '/META-INF')

        # Generate mimetype

        try:
            with open(self.TEMPDIR + '/mimetype', 'w', encoding='utf-8') as f:
                f.write(self._MIMETYPE)
        except:
            return 'ERROR: Cannot write "mimetype"'

        # Generate settings.xml

        try:
            with open(self.TEMPDIR + '/settings.xml', 'w', encoding='utf-8') as f:
                f.write(self._SETTINGS_XML)
        except:
            return 'ERROR: Cannot write "settings.xml"'

        # Generate META-INF\manifest.xml

        try:
            with open(self.TEMPDIR + '/META-INF/manifest.xml', 'w', encoding='utf-8') as f:
                f.write(self._MANIFEST_XML)
        except:
            return 'ERROR: Cannot write "manifest.xml"'

        # Generate styles.xml with system language set as document language

        localeCodes = locale.getdefaultlocale()[0].split('_')

        localeMapping = dict(
            Language=localeCodes[0],
            Country=localeCodes[1],
        )
        template = Template(self._STYLES_XML)
        text = template.safe_substitute(localeMapping)

        try:
            with open(self.TEMPDIR + '/styles.xml', 'w', encoding='utf-8') as f:
                f.write(text)
        except:
            return 'ERROR: Cannot write "styles.xml"'

        # Generate meta.xml with actual document metadata

        dt = datetime.today()

        metaMapping = dict(
            Author=self.author,
            Title=self.title,
            Summary='<![CDATA[' + self.desc + ']]>',
            Date=str(dt.year) + '-' + str(dt.month).rjust(2, '0') +
            '-' + str(dt.day).rjust(2, '0'),
            Time=str(dt.hour).rjust(2, '0') +
            ':' + str(dt.minute).rjust(2, '0') +
            ':' + str(dt.second).rjust(2, '0'),
        )
        template = Template(self._META_XML)
        text = template.safe_substitute(metaMapping)

        try:
            with open(self.TEMPDIR + '/meta.xml', 'w', encoding='utf-8') as f:
                f.write(text)
        except:
            return 'ERROR: Cannot write "meta.xml".'

        return 'SUCCESS: ODF structure generated.'
