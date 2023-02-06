"""Provide a converter class for universal export from a yWriter 7 project. 

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.converter.yw_cnv_ff import YwCnvFf
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


class Yw7Exporter(YwCnvFf):
    """A converter for universal export from a yWriter 7 project.

    Instantiate a Yw7File object as sourceFile and a
    Novel subclass object as targetFile for file conversion.

    Overrides the superclass constants EXPORT_SOURCE_CLASSES, EXPORT_TARGET_CLASSES.    
    """
    EXPORT_SOURCE_CLASSES = [Yw7File]
    EXPORT_TARGET_CLASSES = [OdtWProof,
                             OdtWManuscript,
                             OdtWBriefSynopsis,
                             OdtWSceneDesc,
                             OdtWChapterDesc,
                             OdtWPartDesc,
                             OdtWExport,
                             OdtWCharacters,
                             OdtWItems,
                             OdtWLocations,
                             OdtWXref,
                             OdtWNotes,
                             OdtWTodo,
                             OdsWCharList,
                             OdsWLocList,
                             OdsWItemList,
                             OdsWSceneList,
                             ]
