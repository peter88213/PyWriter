"""Provide an interface emulation for conversion object factory classes.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os

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


class ExportTargetFactory:
    """Base class for conversion object factory classes.

    This class emulates a "FileFactory" Interface.
    """

    def __init__(self):
        self.expTargets = [OdtProof, OdtManuscript, OdtSceneDesc, OdtChapterDesc,
                           OdtPartDesc, OdtExport, OdtCharacters, OdtItems, OdtLocations, OdtXref,
                           OdsCharList, OdsLocList, OdsItemList, OdsSceneList, OdsPlotList]

    def make_file_objects(self, sourcePath, suffix=None):
        """Return source and target objects for conversion, and a message.

        Factory method to be overwritten by subclasses.
        Return a tuple with three elements:
        - A message string starting with 'SUCCESS' or 'ERROR'
        - sourceFile: a Novel subclass instance
        - targetFile: a Novel subclass instance
        """
        fileName, fileExtension = os.path.splitext(sourcePath)

        if suffix is None:
            targetFile = Yw5File(fileName + Yw5File.EXTENSION)
            targetFile.ywTreeBuilder = Yw5TreeCreator()
            targetFile.ywProjectMerger = YwProjectCreator()
            return 'SUCCESS', None, targetFile

        for expTarget in self.expTargets:
            if expTarget.SUFFIX == suffix:
                targetFile = expTarget(fileName + suffix + expTarget.EXTENSION)
                return 'SUCCESS', None, targetFile

        return 'ERROR: File type of "' + os.path.normpath(sourcePath) + '" not supported.', None, None
