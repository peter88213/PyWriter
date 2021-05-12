"""Provide an interface emulation for conversion object factory classes.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os

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


class ImportObjectsFactory:
    """Base class for conversion object factory classes.

    This class emulates a "FileFactory" Interface.
    """

    def __init__(self):
        self.impTargets = [Yw7File, Yw6File, Yw5File]

    def make_file_objects(self, sourcePath, suffix=None):
        """Return source and target objects for conversion, and a message.

        Factory method to be overwritten by subclasses.
        Return a tuple with three elements:
        - A message string starting with 'SUCCESS' or 'ERROR'
        - sourceFile: a Novel subclass instance
        - targetFile: a Novel subclass instance
        """
        fileName, fileExtension = os.path.splitext(sourcePath)

        for impTarget in self.impTargets:
            if impTarget.EXTENSION == fileExtension:
                sourceFile = impTarget(sourcePath)
                return 'SUCCESS', sourceFile, None

        return 'ERROR: File type of "' + os.path.normpath(sourcePath) + '" not supported.', None, None
