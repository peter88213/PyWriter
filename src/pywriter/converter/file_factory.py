"""A simple file factory. 

Instantiate the Novel subclass objects 
sourceFile and targetFile for file conversion.

Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os

from pywriter.yw.yw5_file import Yw5File
from pywriter.yw.yw6_file import Yw6File
from pywriter.yw.yw7_file import Yw7File
from pywriter.yw.yw7_tree_creator import Yw7TreeCreator
from pywriter.yw.yw5_tree_creator import Yw5TreeCreator

from pywriter.odt.odt_proof import OdtProof
from pywriter.odt.odt_manuscript import OdtManuscript
from pywriter.odt.odt_scenedesc import OdtSceneDesc
from pywriter.odt.odt_chapterdesc import OdtChapterDesc
from pywriter.odt.odt_partdesc import OdtPartDesc
from pywriter.odt.odt_export import OdtExport
from pywriter.odt.odt_characters import OdtCharacters
from pywriter.odt.odt_items import OdtItems
from pywriter.odt.odt_locations import OdtLocations

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


class FileFactory():
    """A simple factory class that instantiates a source file object
    and a target file object for conversion.
    """

    YW_EXTENSIONS = ['.yw5', '.yw6', '.yw7']

    def get_file_objects(self, sourcePath, suffix=None):
        fileName, fileExtension = os.path.splitext(sourcePath)
        isYwProject = False

        if fileExtension == Yw7File.EXTENSION:
            sourceFile = Yw7File(sourcePath)
            isYwProject = True

        elif fileExtension == Yw5File.EXTENSION:
            sourceFile = Yw5File(sourcePath)
            isYwProject = True

        elif fileExtension == Yw6File.EXTENSION:
            sourceFile = Yw6File(sourcePath)
            isYwProject = True

        if isYwProject:

            # Determine which sort of target is required.

            if suffix is None:
                targetFile = Yw5File(fileName + Yw5File.EXTENSION)
                targetFile.ywTreeBuilder = Yw5TreeCreator()

            elif suffix == '':
                targetFile = OdtExport(fileName + OdtExport.EXTENSION)

            elif suffix == OdtManuscript.SUFFIX:
                targetFile = OdtManuscript(
                    fileName + suffix + OdtManuscript.EXTENSION)

            elif suffix == OdtProof.SUFFIX:
                targetFile = OdtProof(fileName + suffix + OdtProof.EXTENSION)

            elif suffix == OdtSceneDesc.SUFFIX:
                targetFile = OdtSceneDesc(
                    fileName + suffix + OdtSceneDesc.EXTENSION)

            elif suffix == OdtChapterDesc.SUFFIX:
                targetFile = OdtChapterDesc(
                    fileName + suffix + OdtChapterDesc.EXTENSION)

            elif suffix == OdtPartDesc.SUFFIX:
                targetFile = OdtPartDesc(
                    fileName + suffix + OdtPartDesc.EXTENSION)

            elif suffix == OdtCharacters.SUFFIX:
                targetFile = OdtCharacters(
                    fileName + suffix + OdtCharacters.EXTENSION)

            elif suffix == OdtLocations.SUFFIX:
                targetFile = OdtLocations(
                    fileName + suffix + OdtLocations.EXTENSION)

            elif suffix == OdtItems.SUFFIX:
                targetFile = OdtItems(fileName + suffix + OdtItems.EXTENSION)

            elif suffix == CsvSceneList.SUFFIX:
                targetFile = CsvSceneList(
                    fileName + suffix + CsvSceneList.EXTENSION)

            elif suffix == CsvPlotList.SUFFIX:
                targetFile = CsvPlotList(
                    fileName + suffix + CsvPlotList.EXTENSION)

            elif suffix == CsvCharList.SUFFIX:
                targetFile = CsvCharList(
                    fileName + suffix + CsvCharList.EXTENSION)

            elif suffix == CsvLocList.SUFFIX:
                targetFile = CsvLocList(
                    fileName + suffix + CsvLocList.EXTENSION)

            elif suffix == CsvItemList.SUFFIX:
                targetFile = CsvItemList(
                    fileName + suffix + CsvItemList.EXTENSION)

            else:
                return ['ERROR: File type of "' + os.path.normpath(sourcePath) + '" not supported.', None, None]

        else:
            # The source file is not a yWriter project.

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

            elif sourcePath.endswith('.html'):

                # Is the source file an outline or a "work in progress"?

                result = read_html_file(sourcePath)

                if 'SUCCESS' in result[0]:

                    if "<h3" in result[1].lower():
                        sourceFile = HtmlOutline(sourcePath)

                    else:
                        sourceFile = HtmlImport(sourcePath)
                        targetFile = Yw7File(fileName + Yw7File.EXTENSION)
                        targetFile.ywTreeBuilder = Yw7TreeCreator()

                else:
                    return ['ERROR: Cannot read "' + os.path.normpath(sourcePath) + '".', None, None]

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
                return ['ERROR: File type of  "' + os.path.normpath(sourcePath) + '" not supported.', None, None]

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
                return ['ERROR: No yWriter project to write.', None, None]

        return ('SUCCESS', sourceFile, targetFile)
