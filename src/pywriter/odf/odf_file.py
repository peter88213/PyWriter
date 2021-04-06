"""OdfFile - Generic Class for OpenDocument xml file generation.

Part of the PyWriter project.
Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import zipfile
import locale
from shutil import rmtree
from datetime import datetime
from string import Template

from pywriter.file.file_export import FileExport


class OdfFile(FileExport):
    """OpenDocument xml project file representation.
    """

    TEMPDIR = 'temp_odf'

    ODF_COMPONENTS = []
    _MIMETYPE = ''
    _SETTINGS_XML = ''
    _MANIFEST_XML = ''
    _STYLES_XML = ''
    _META_XML = ''

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

    def write(self):
        """Generate an odf file from a template.
        Return a message beginning with SUCCESS or ERROR.
        """

        # Create a temporary directory containing the internal
        # structure of an ODS file except "content.xml".

        message = self.set_up()

        if message.startswith('ERROR'):
            return message

        # Add "content.xml" to the temporary directory.

        filePath = self._filePath

        self._filePath = self.TEMPDIR + '/content.xml'

        message = FileExport.write(self)

        self._filePath = filePath

        if message.startswith('ERROR'):
            return message

        # Pack the contents of the temporary directory
        # into the ODF file.

        workdir = os.getcwd()

        try:
            with zipfile.ZipFile(self.filePath, 'w') as odfTarget:
                os.chdir(self.TEMPDIR)

                for file in self.ODF_COMPONENTS:
                    odfTarget.write(file, compress_type=zipfile.ZIP_DEFLATED)
        except:
            os.chdir(workdir)
            return 'ERROR: Cannot generate "' + os.path.normpath(self.filePath) + '".'

        # Remove temporary data.

        os.chdir(workdir)
        self.tear_down()
        return 'SUCCESS: "' + os.path.normpath(self.filePath) + '" written.'
