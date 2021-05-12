"""Provide a factory class for import source and target objects.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os

from pywriter.converter.file_factory import FileFactory

from pywriter.yw.yw5_file import Yw5File
from pywriter.yw.yw6_file import Yw6File
from pywriter.yw.yw7_file import Yw7File
from pywriter.yw.yw7_tree_creator import Yw7TreeCreator
from pywriter.yw.yw_project_creator import YwProjectCreator


from pywriter.html.html_import import HtmlImport
from pywriter.html.html_outline import HtmlOutline
from pywriter.odt.odt_xref import OdtXref

from pywriter.html.html_fop import read_html_file


class ImportObjectsFactory(FileFactory):
    """A factory class that instantiates source and target file objects."""

    def __init__(self):
        self.impSources = []
        # List of FileExport subclasses. To be set by the caller.

    def make_file_objects(self, sourcePath, suffix=None):
        """Factory method.
        Return a tuple with three elements:
        - A message string starting with 'SUCCESS' or 'ERROR'
        - sourceFile: a Novel subclass instance
        - targetFile: a Novel subclass instance

        """
        fileName, fileExtension = os.path.splitext(sourcePath)
        sourceFile = None
        targetFile = None

        for impSource in self.impSources:

            if sourcePath.endswith(impSource.SUFFIX + impSource.EXTENSION):
                sourceFile = impSource(sourcePath)

        if sourceFile is None:

            if (OdtXref.SUFFIX + '.' in sourcePath):
                return 'ERROR: Cross references are not meant to be written back.', None, None

            elif sourcePath.endswith('.html'):

                # The source file might be an outline or a "work in progress".

                result = read_html_file(sourcePath)

                if result[0].startswith('SUCCESS'):
                    targetFile = Yw7File(fileName + Yw7File.EXTENSION)
                    targetFile.ywTreeBuilder = Yw7TreeCreator()
                    targetFile.ywProjectMerger = YwProjectCreator()

                    if "<h3" in result[1].lower():
                        sourceFile = HtmlOutline(sourcePath)

                    else:
                        sourceFile = HtmlImport(sourcePath)

                else:
                    return 'ERROR: Cannot read "' + os.path.normpath(sourcePath) + '".', None, None

            else:
                return 'ERROR: File type of  "' + os.path.normpath(sourcePath) + '" not supported.', None, None

        if targetFile is None:

            ywPathBasis = fileName.split(sourceFile.SUFFIX)[0]

            # Look for an existing yWriter project to rewrite.

            if os.path.isfile(ywPathBasis + Yw7File.EXTENSION):
                targetFile = Yw7File(ywPathBasis + Yw7File.EXTENSION)

            elif os.path.isfile(ywPathBasis + Yw5File.EXTENSION):
                targetFile = Yw5File(ywPathBasis + Yw5File.EXTENSION)

            elif os.path.isfile(ywPathBasis + Yw6File.EXTENSION):
                targetFile = Yw6File(ywPathBasis + Yw6File.EXTENSION)

        if targetFile is None:
            return 'ERROR: No yWriter project to write.', None, None

        return 'SUCCESS', sourceFile, targetFile
