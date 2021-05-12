"""Provide a factory class for export from yWriter 7. 

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.converter.file_factory import FileFactory
from pywriter.converter.abstract_file_factory import AbstractFileFactory
from pywriter.converter.yw7_source_factory import Yw7SourceFactory
from pywriter.converter.export_target_factory import ExportTargetFactory

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


class ExportFileFactory(AbstractFileFactory):
    """A factory class that instantiates the file objects for conversion.

    Instantiate a Yw7File object as sourceFile and a
    Novel subclass object as targetFile for file conversion.
    """

    def __init__(self):
        """Set the instance variables for the abstract factory.

        Override the AbstractFileFactory constructor.

        exportSourceFactory (default: ExportSourceFactory)
        exportTargetFactory (default: ExportTargetFactory)
        """
        self.exportSourceFactory = Yw7SourceFactory()
        self.exportTargetFactory = ExportTargetFactory()
        self.exportTargetFactory.expTargets = [OdtProof, OdtManuscript, OdtSceneDesc, OdtChapterDesc,
                                               OdtPartDesc, OdtExport, OdtCharacters, OdtItems, OdtLocations, OdtXref,
                                               OdsCharList, OdsLocList, OdsItemList, OdsSceneList, OdsPlotList]
        self.importObjectsFactory = FileFactory()
