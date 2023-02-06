"""Provide a converter class for yWriter 7 universal import and export.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.converter.yw_cnv_ff import YwCnvFf
from pywriter.converter.new_project_factory import NewProjectFactory
from pywriter.yw.yw7_file import Yw7File
from pywriter.odt.odt_w_proof import OdtWProof
from pywriter.odt.odt_w_manuscript import OdtWManuscript
from pywriter.odt.odt_w_scenedesc import OdtWSceneDesc
from pywriter.odt.odt_w_chapterdesc import OdtWChapterDesc
from pywriter.odt.odt_w_partdesc import OdtWPartDesc
from pywriter.odt.odt_w_brief_synopsis import OdtWBriefSynopsis
from pywriter.odt.odt_w_export import OdtWExport
from pywriter.odt.odt_w_characters import OdtWCharacters
from pywriter.odt.odt_w_items import OdtWItems
from pywriter.odt.odt_w_locations import OdtWLocations
from pywriter.odt.odt_w_xref import OdtWXref
from pywriter.odt.odt_w_notes import OdtWNotes
from pywriter.odt.odt_w_todo import OdtWTodo
from pywriter.ods.ods_w_charlist import OdsWCharList
from pywriter.ods.ods_w_loclist import OdsWLocList
from pywriter.ods.ods_w_itemlist import OdsWItemList
from pywriter.ods.ods_w_scenelist import OdsWSceneList
from pywriter.html.html_proof import HtmlProof
from pywriter.html.html_manuscript import HtmlManuscript
from pywriter.html.html_notes import HtmlNotes
from pywriter.html.html_todo import HtmlTodo
from pywriter.html.html_scenedesc import HtmlSceneDesc
from pywriter.html.html_chapterdesc import HtmlChapterDesc
from pywriter.html.html_partdesc import HtmlPartDesc
from pywriter.html.html_characters import HtmlCharacters
from pywriter.html.html_locations import HtmlLocations
from pywriter.html.html_items import HtmlItems
from pywriter.ods.ods_r_scenelist import OdsRSceneList
from pywriter.ods.ods_r_charlist import OdsRCharList
from pywriter.ods.ods_r_loclist import OdsRLocList
from pywriter.ods.ods_r_itemlist import OdsRItemList


class Yw7Converter(YwCnvFf):
    """A converter for universal import and export.

    Support yWriter 7 projects and most of the Novel subclasses 
    that can be read or written by OpenOffice/LibreOffice.

    Overrides the superclass constants EXPORT_SOURCE_CLASSES,
    EXPORT_TARGET_CLASSES, IMPORT_SOURCE_CLASSES, IMPORT_TARGET_CLASSES.

    Class constants:
        CREATE_SOURCE_CLASSES -- list of classes that - additional to HtmlImport
                        and HtmlOutline - can be exported to a new yWriter project.
    """
    EXPORT_SOURCE_CLASSES = [Yw7File]
    EXPORT_TARGET_CLASSES = [OdtWExport,
                             OdtWProof,
                             OdtWManuscript,
                             OdtWBriefSynopsis,
                             OdtWSceneDesc,
                             OdtWChapterDesc,
                             OdtWPartDesc,
                             OdtWCharacters,
                             OdtWItems,
                             OdtWLocations,
                             OdsWCharList,
                             OdsWLocList,
                             OdsWItemList,
                             OdsWSceneList,
                             OdtWXref,
                             OdtWNotes,
                             OdtWTodo,
                             ]
    IMPORT_SOURCE_CLASSES = [HtmlProof,
                             HtmlManuscript,
                             HtmlSceneDesc,
                             HtmlChapterDesc,
                             HtmlPartDesc,
                             HtmlCharacters,
                             HtmlItems,
                             HtmlLocations,
                             HtmlNotes,
                             HtmlTodo,
                             OdsRCharList,
                             OdsRLocList,
                             OdsRItemList,
                             OdsRSceneList,
                             ]
    IMPORT_TARGET_CLASSES = [Yw7File]
    CREATE_SOURCE_CLASSES = []

    def __init__(self):
        """Change the newProjectFactory strategy.
        
        Extends the superclass constructor.
        """
        super().__init__()
        self.newProjectFactory = NewProjectFactory(self.CREATE_SOURCE_CLASSES)
