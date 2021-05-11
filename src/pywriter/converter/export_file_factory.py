"""An export file factory. 

Instantiate the Novel subclass objects 
sourceFile and targetFile for file conversion.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os

from pywriter.converter.file_factory import FileFactory

from pywriter.yw.yw5_file import Yw5File
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
from pywriter.odt.odt_xref import OdtXref

from pywriter.ods.ods_charlist import OdsCharList
from pywriter.ods.ods_loclist import OdsLocList
from pywriter.ods.ods_itemlist import OdsItemList
from pywriter.ods.ods_scenelist import OdsSceneList
from pywriter.ods.ods_plotlist import OdsPlotList


class ExportFileFactory(FileFactory):
    """A factory class that instantiates a source file object
    and a target file object for conversion.
    All filetypes to be exported from yWriter are covered.
    """

    def make_export_target(self, sourcePath, suffix):
        """

        This is a primitive operation of the make_file_objects() template method.

        """
        # Determine which sort of target is required.

        fileName, fileExtension = os.path.splitext(sourcePath)

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

        elif suffix == OdtXref.SUFFIX:
            targetFile = OdtXref(fileName + suffix + OdtXref.EXTENSION)

        elif suffix == OdsSceneList.SUFFIX:
            targetFile = OdsSceneList(
                fileName + suffix + OdsSceneList.EXTENSION)

        elif suffix == OdsPlotList.SUFFIX:
            targetFile = OdsPlotList(
                fileName + suffix + OdsPlotList.EXTENSION)

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
            targetFile = None

        return targetFile

    def make_import_objects(self, sourcePath):
        """Factory method.
        Return a tuple with three elements:
        - A message string starting with 'SUCCESS' or 'ERROR'
        - sourceFile: a Novel subclass instance
        - targetFile: a Novel subclass instance

        This is a primitive operation of the make_file_objects() template method.

        """
        return 'ERROR: Source is not a yWriter project.', None, None
