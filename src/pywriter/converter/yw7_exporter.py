"""Provide a converter class for universal export from a yWriter 7 project. 

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.converter.yw_cnv_ff import YwCnvFf

from pywriter.yw.yw7_file import Yw7File

from pywriter.odt.odt_proof import OdtProof
from pywriter.odt.odt_manuscript import OdtManuscript
from pywriter.odt.odt_scenedesc import OdtSceneDesc
from pywriter.odt.odt_chapterdesc import OdtChapterDesc
from pywriter.odt.odt_partdesc import OdtPartDesc
from pywriter.odt.odt_brief_synopsis import OdtBriefSynopsis
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


class Yw7Exporter(YwCnvFf):
    """A converter for universal export from a yWriter 7 project.

    Instantiate a Yw7File object as sourceFile and a
    Novel subclass object as targetFile for file conversion.

    Override the superclass constants EXPORT_SOURCE_CLASSES, EXPORT_TARGET_CLASSES.    
    """
    EXPORT_SOURCE_CLASSES = [Yw7File]

    EXPORT_TARGET_CLASSES = [OdtProof,
                             OdtManuscript,
                             OdtBriefSynopsis,
                             OdtSceneDesc,
                             OdtChapterDesc,
                             OdtPartDesc,
                             OdtExport,
                             OdtCharacters,
                             OdtItems,
                             OdtLocations,
                             OdtXref,
                             OdsCharList,
                             OdsLocList,
                             OdsItemList,
                             OdsSceneList,
                             OdsPlotList]
