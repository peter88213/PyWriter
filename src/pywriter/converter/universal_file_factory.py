"""Provide a factory class for universal import and export.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.converter.abstract_file_factory import AbstractFileFactory
from pywriter.converter.yw7_source_factory import Yw7SourceFactory
from pywriter.converter.export_target_factory import ExportTargetFactory
from pywriter.converter.import_objects_factory import ImportObjectsFactory

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


class UniversalFileFactory(AbstractFileFactory):
    """A factory class that instantiates the file objects for conversion.

    Support yWriter 7 projects and most of the Novel subclasses 
    that can be read or written by OpenOffice/LibreOffice. 
    """

    def __init__(self):
        """Set the instance variables for the abstract factory.

        Override the AbstractFileFactory constructor.

        exportSourceFactory (default: Yw7SourceFactory)
        exportTargetFactory (default: ExportTargetFactory)
        importObjectsFactory (default: ImportObjectsFactory)
        """
        self.exportSourceFactory = Yw7SourceFactory()
        self.exportTargetFactory = ExportTargetFactory()
        self.exportTargetFactory.expTargets = [OdtExport,
                                               OdtProof,
                                               OdtManuscript,
                                               OdtSceneDesc,
                                               OdtChapterDesc,
                                               OdtPartDesc,
                                               OdtCharacters,
                                               OdtItems,
                                               OdtLocations,
                                               OdsCharList,
                                               OdsLocList,
                                               OdsItemList,
                                               OdsSceneList,
                                               OdsPlotList,
                                               OdtXref,
                                               ]
        self.importObjectsFactory = ImportObjectsFactory()
        self.importObjectsFactory.impSources = [HtmlProof,
                                                HtmlManuscript,
                                                HtmlSceneDesc,
                                                HtmlChapterDesc,
                                                HtmlPartDesc,
                                                HtmlCharacters,
                                                HtmlItems,
                                                HtmlLocations,
                                                CsvCharList,
                                                CsvLocList,
                                                CsvItemList,
                                                CsvSceneList,
                                                CsvPlotList,
                                                ]
