"""Provide a factory class for import source and target objects.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os

from pywriter.converter.file_factory import FileFactory

from pywriter.yw.yw7_new_file import Yw7NewFile
from pywriter.html.html_import import HtmlImport
from pywriter.html.html_outline import HtmlOutline

from pywriter.html.html_fop import read_html_file


class NewProjectFactory(FileFactory):
    """A factory class that instantiates source and target file objects."""

    DO_NOT_IMPORT = ['_xref']

    def make_file_objects(self, sourcePath, **kwargs):
        """Factory method.
        Return a tuple with three elements:
        - A message string starting with 'SUCCESS' or 'ERROR'
        - sourceFile: a Novel subclass instance
        - targetFile: a Novel subclass instance

        """
        if not self.canImport(sourcePath):
            return 'ERROR: This document is not meant to be written back.', None, None

        if sourcePath.endswith('.html'):

            # The source file might be an outline or a "work in progress".

            result = read_html_file(sourcePath)

            if result[0].startswith('SUCCESS'):
                fileName, fileExtension = os.path.splitext(sourcePath)
                targetFile = Yw7NewFile(
                    fileName + Yw7NewFile.EXTENSION, **kwargs)

                if "<h3" in result[1].lower():
                    sourceFile = HtmlOutline(sourcePath, **kwargs)

                else:
                    sourceFile = HtmlImport(sourcePath, **kwargs)

            else:
                return 'ERROR: Cannot read "' + os.path.normpath(sourcePath) + '".', None, None

        else:
            return 'ERROR: File type of  "' + os.path.normpath(sourcePath) + '" not supported.', None, None

        return 'SUCCESS', sourceFile, targetFile

    def canImport(self, sourcePath):
        fileName, fileExtension = os.path.splitext(sourcePath)

        for suffix in self.DO_NOT_IMPORT:

            if fileName.endswith(suffix):
                return False

        return True
