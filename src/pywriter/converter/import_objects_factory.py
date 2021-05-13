"""Provide a factory class for import source and target objects.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os

from pywriter.converter.file_factory import FileFactory
from pywriter.converter.source_file_factory import SourceFileFactory
from pywriter.converter.import_target_factory import ImportTargetFactory

from pywriter.yw.yw7_new_file import Yw7NewFile


from pywriter.html.html_import import HtmlImport
from pywriter.html.html_outline import HtmlOutline
from pywriter.odt.odt_xref import OdtXref

from pywriter.html.html_fop import read_html_file


class ImportObjectsFactory(FileFactory):
    """A factory class that instantiates source and target file objects."""

    def __init__(self, sourceClasses=[], targetClasses=[]):
        self.sourceClasses = sourceClasses
        self.targetClasses = targetClasses

    def make_file_objects(self, sourcePath, suffix=None):
        """Factory method.
        Return a tuple with three elements:
        - A message string starting with 'SUCCESS' or 'ERROR'
        - sourceFile: a Novel subclass instance
        - targetFile: a Novel subclass instance

        """
        fileName, fileExtension = os.path.splitext(sourcePath)

        factory = SourceFileFactory(self.sourceClasses)

        message, sourceFile, targetFile = factory.make_file_objects(sourcePath)

        if sourceFile is None:

            if (OdtXref.SUFFIX + '.' in sourcePath):
                return 'ERROR: Cross references are not meant to be written back.', None, None

            elif sourcePath.endswith('.html'):

                # The source file might be an outline or a "work in progress".

                result = read_html_file(sourcePath)

                if result[0].startswith('SUCCESS'):
                    targetFile = Yw7NewFile(fileName + Yw7NewFile.EXTENSION)

                    if "<h3" in result[1].lower():
                        sourceFile = HtmlOutline(sourcePath)

                    else:
                        sourceFile = HtmlImport(sourcePath)

                else:
                    return 'ERROR: Cannot read "' + os.path.normpath(sourcePath) + '".', None, None

            else:
                return 'ERROR: File type of  "' + os.path.normpath(sourcePath) + '" not supported.', None, None

        if targetFile is None:
            factory = ImportTargetFactory(self.targetClasses)

            message, dummy, targetFile = factory.make_file_objects(
                sourcePath, sourceFile.SUFFIX)

            if message.startswith('ERROR'):
                return message, None, None

        return 'SUCCESS', sourceFile, targetFile
