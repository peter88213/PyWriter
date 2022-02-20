"""Provide a generic class for OpenDocument xml file export.

All ODS and ODT file representations inherit from this class.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import zipfile
import locale
import tempfile
from shutil import rmtree
from datetime import datetime
from string import Template

from pywriter.pywriter_globals import ERROR
from pywriter.file.file_export import FileExport


class OdfFile(FileExport):
    """Generic OpenDocument xml file representation.

    Public methods:
        write() -- write instance variables to the export file.
    """
    _ODF_COMPONENTS = []
    _MIMETYPE = ''
    _SETTINGS_XML = ''
    _MANIFEST_XML = ''
    _STYLES_XML = ''
    _META_XML = ''

    def __init__(self, filePath, **kwargs):
        """Create a temporary directory for zipfile generation.
        
        Positional arguments:
            filePath -- str: path to the file represented by the Novel instance.
            
        Optional arguments:
            kwargs -- keyword arguments to be used by subclasses.            

        Extends the superclass constructor,        
        """
        super().__init__(filePath, **kwargs)
        self._tempDir = tempfile.mkdtemp(suffix='.tmp', prefix='odf_')
        self._originalPath = self._filePath

    def __del__(self):
        """Make sure to delete the temporary directory, in case write() has not been called."""
        self._tear_down()

    def _tear_down(self):
        """Delete the temporary directory containing the unpacked ODF directory structure."""
        try:
            rmtree(self._tempDir)
        except:
            pass

    def _set_up(self):
        """Helper method for ZIP file generation.

        Prepare the temporary directory containing the internal structure of an ODF file except 'content.xml'.
        Return a message beginning with the ERROR constant in case of error.
        """
        
        # Create and open a temporary directory for the files to zip.

        try:
            self._tear_down()
            os.mkdir(self._tempDir)
            os.mkdir(f'{self._tempDir}/META-INF')

        except:
            return f'{ERROR}Cannot create "{os.path.normpath(self._tempDir)}".'

        # Generate mimetype.

        try:
            with open(f'{self._tempDir}/mimetype', 'w', encoding='utf-8') as f:
                f.write(self._MIMETYPE)
        except:
            return f'{ERROR}Cannot write "mimetype"'

        # Generate settings.xml.

        try:
            with open(f'{self._tempDir}/settings.xml', 'w', encoding='utf-8') as f:
                f.write(self._SETTINGS_XML)
        except:
            return f'{ERROR}Cannot write "settings.xml"'

        # Generate META-INF\manifest.xml.

        try:
            with open(f'{self._tempDir}/META-INF/manifest.xml', 'w', encoding='utf-8') as f:
                f.write(self._MANIFEST_XML)
        except:
            return f'{ERROR}Cannot write "manifest.xml"'

        # Generate styles.xml with system language set as document language.

        lng, ctr = locale.getdefaultlocale()[0].split('_')
        localeMapping = dict(
            Language=lng,
            Country=ctr,
        )
        template = Template(self._STYLES_XML)
        text = template.safe_substitute(localeMapping)

        try:
            with open(f'{self._tempDir}/styles.xml', 'w', encoding='utf-8') as f:
                f.write(text)
        except:
            return f'{ERROR}Cannot write "styles.xml"'

        # Generate meta.xml with actual document metadata.

        metaMapping = dict(
            Author=self.authorName,
            Title=self.title,
            Summary=f'<![CDATA[{self.desc}]]>',
            Datetime=datetime.today().replace(microsecond=0).isoformat(),
        )
        template = Template(self._META_XML)
        text = template.safe_substitute(metaMapping)

        try:
            with open(f'{self._tempDir}/meta.xml', 'w', encoding='utf-8') as f:
                f.write(text)
        except:
            return f'{ERROR}Cannot write "meta.xml".'

        return 'ODF structure generated.'

    def write(self):
        """Write instance variables to the export file.
        
        Create a template-based output file. 
        Return a message beginning with the ERROR constant in case of error.
        Extends the super class method, adding ZIP file operations.
        """

        # Create a temporary directory containing the internal
        # structure of an ODS file except "content.xml".

        message = self._set_up()

        if message.startswith(ERROR):
            return message

        # Add "content.xml" to the temporary directory.

        self._originalPath = self._filePath

        self._filePath = f'{self._tempDir}/content.xml'

        message = super().write()

        self._filePath = self._originalPath

        if message.startswith(ERROR):
            return message

        # Pack the contents of the temporary directory
        # into the ODF file.

        workdir = os.getcwd()
        backedUp = False

        if os.path.isfile(self.filePath):

            try:
                os.replace(self.filePath, f'{self.filePath}.bak')
                backedUp = True
                
            except:
                return f'{ERROR}Cannot overwrite "{os.path.normpath(self.filePath)}".'
            
        try:
            with zipfile.ZipFile(self.filePath, 'w') as odfTarget:
                os.chdir(self._tempDir)

                for file in self._ODF_COMPONENTS:
                    odfTarget.write(file, compress_type=zipfile.ZIP_DEFLATED)
        except:

            if backedUp:
                os.replace(f'{self.filePath}.bak', self.filePath)

            os.chdir(workdir)
            return f'{ERROR}Cannot generate "{os.path.normpath(self.filePath)}".'

        # Remove temporary data.

        os.chdir(workdir)
        self._tear_down()
        return f'"{os.path.normpath(self.filePath)}" written.'
