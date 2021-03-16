"""An export file factory. 

Instantiate the Novel subclass objects 
sourceFile and targetFile for file conversion.

Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os

from pywriter.converter.file_factory import FileFactory

from pywriter.yw.yw5_file import Yw5File
from pywriter.yw.yw6_file import Yw6File
from pywriter.yw.yw7_file import Yw7File
from pywriter.yw.yw5_tree_creator import Yw5TreeCreator
from pywriter.yw.yw_project_creator import YwProjectCreator

from pywriter.odt.odt_proof import OdtProof
from pywriter.odt.odt_manuscript import OdtManuscript
from pywriter.odt.odt_scenedesc import OdtSceneDesc
from pywriter.odt.odt_chapterdesc import OdtChapterDesc
from pywriter.odt.odt_partdesc import OdtPartDesc
from pywriter.odt.odt_export import OdtExport
from pywriter.odt.odt_characters import OdtCharacters
from pywriter.odt.odt_items import OdtItems
from pywriter.odt.odt_locations import OdtLocations

from pywriter.csv.csv_plotlist import CsvPlotList

from pywriter.ods.ods_charlist import OdsCharList
from pywriter.ods.ods_loclist import OdsLocList
from pywriter.ods.ods_itemlist import OdsItemList
from pywriter.ods.ods_scenelist import OdsSceneList


class ExportFileFactory(FileFactory):
    """A factory class that instantiates a source file object
    and a target file object for conversion.
    All filetypes to be exported from yWriter are covered.
    """

    def get_file_objects(self, sourcePath, suffix=None):
        """Return a tuple with three elements:
        * A message string starting with 'SUCCESS' or 'ERROR'
        * sourceFile: a Novel subclass instance
        * targetFile: a Novel subclass instance
        """
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
                targetFile.ywProjectMerger = YwProjectCreator()

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

            elif suffix == OdsSceneList.SUFFIX:
                targetFile = OdsSceneList(
                    fileName + suffix + OdsSceneList.EXTENSION)

            elif suffix == CsvPlotList.SUFFIX:
                targetFile = CsvPlotList(
                    fileName + suffix + CsvPlotList.EXTENSION)

            elif suffix == OdsCharList.SUFFIX:
                targetFile = OdsCharList(
                    fileName + suffix + OdsCharList.EXTENSION)

            elif suffix == OdsLocList.SUFFIX:
                targetFile = OdsLocList(
                    fileName + suffix + OdsLocList.EXTENSION)

            elif suffix == OdsItemList.SUFFIX:
                targetFile = OdsItemList(
                    fileName + suffix + OdsItemList.EXTENSION)

            else:
                return 'ERROR: File type of "' + os.path.normpath(sourcePath) + '" not supported.', None, None

        else:
            # The source file is not a yWriter project.

            return 'ERROR: Source is not a yWriter project.', None, None

        return 'SUCCESS', sourceFile, targetFile
