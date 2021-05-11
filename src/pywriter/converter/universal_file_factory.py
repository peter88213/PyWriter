"""UniversalFileFactory - Instantiate the objects for file conversion. 

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os

from pywriter.converter.export_file_factory import ExportFileFactory

from pywriter.yw.yw5_file import Yw5File
from pywriter.yw.yw6_file import Yw6File
from pywriter.yw.yw7_file import Yw7File
from pywriter.yw.yw7_tree_creator import Yw7TreeCreator
from pywriter.yw.yw_project_creator import YwProjectCreator

from pywriter.odt.odt_xref import OdtXref

from pywriter.html.html_proof import HtmlProof
from pywriter.html.html_manuscript import HtmlManuscript
from pywriter.html.html_scenedesc import HtmlSceneDesc
from pywriter.html.html_chapterdesc import HtmlChapterDesc
from pywriter.html.html_partdesc import HtmlPartDesc
from pywriter.html.html_characters import HtmlCharacters
from pywriter.html.html_locations import HtmlLocations
from pywriter.html.html_items import HtmlItems
from pywriter.html.html_import import HtmlImport
from pywriter.html.html_outline import HtmlOutline

from pywriter.csv.csv_scenelist import CsvSceneList
from pywriter.csv.csv_plotlist import CsvPlotList
from pywriter.csv.csv_charlist import CsvCharList
from pywriter.csv.csv_loclist import CsvLocList
from pywriter.csv.csv_itemlist import CsvItemList

from pywriter.html.html_fop import read_html_file


class UniversalFileFactory(ExportFileFactory):
    """A factory class that instantiates a source file object
    and a target file object for conversion.
    All file types relevant for OpenOffice/LibreOffice import 
    and export are available.
    """

    def make_import_objects(self, sourcePath):
        """Factory method.
        Return a tuple with three elements:
        - A message string starting with 'SUCCESS' or 'ERROR'
        - sourceFile: a Novel subclass instance
        - targetFile: a Novel subclass instance

        This is a primitive operation of the make_file_objects() template method.

        """
        fileName, fileExtension = os.path.splitext(sourcePath)
        targetFile = None

        if sourcePath.endswith(HtmlProof.SUFFIX + HtmlProof.EXTENSION):
            sourceFile = HtmlProof(sourcePath)

        elif sourcePath.endswith(HtmlManuscript.SUFFIX + HtmlManuscript.EXTENSION):
            sourceFile = HtmlManuscript(sourcePath)

        elif sourcePath.endswith(HtmlSceneDesc.SUFFIX + HtmlSceneDesc.EXTENSION):
            sourceFile = HtmlSceneDesc(sourcePath)

        elif sourcePath.endswith(HtmlChapterDesc.SUFFIX + HtmlChapterDesc.EXTENSION):
            sourceFile = HtmlChapterDesc(sourcePath)

        elif sourcePath.endswith(HtmlPartDesc.SUFFIX + HtmlPartDesc.EXTENSION):
            sourceFile = HtmlPartDesc(sourcePath)

        elif sourcePath.endswith(HtmlCharacters.SUFFIX + HtmlCharacters.EXTENSION):
            sourceFile = HtmlCharacters(sourcePath)

        elif sourcePath.endswith(HtmlLocations.SUFFIX + HtmlLocations.EXTENSION):
            sourceFile = HtmlLocations(sourcePath)

        elif sourcePath.endswith(HtmlItems.SUFFIX + HtmlItems.EXTENSION):
            sourceFile = HtmlItems(sourcePath)

        elif (OdtXref.SUFFIX + '.' in sourcePath):
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

        elif sourcePath.endswith(CsvSceneList.SUFFIX + CsvSceneList.EXTENSION):
            sourceFile = CsvSceneList(sourcePath)

        elif sourcePath.endswith(CsvPlotList.SUFFIX + CsvPlotList.EXTENSION):
            sourceFile = CsvPlotList(sourcePath)

        elif sourcePath.endswith(CsvCharList.SUFFIX + CsvCharList.EXTENSION):
            sourceFile = CsvCharList(sourcePath)

        elif sourcePath.endswith(CsvLocList.SUFFIX + CsvLocList.EXTENSION):
            sourceFile = CsvLocList(sourcePath)

        elif sourcePath.endswith(CsvItemList.SUFFIX + CsvItemList.EXTENSION):
            sourceFile = CsvItemList(sourcePath)

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
