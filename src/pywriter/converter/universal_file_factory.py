"""UniversalFileFactory - Instantiate the objects for file conversion. 

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.converter.abstract_file_factory import AbstractFileFactory
from pywriter.converter.export_source_factory import ExportSourceFactory
from pywriter.converter.export_target_factory import ExportTargetFactory
from pywriter.converter.import_objects_factory import ImportObjectsFactory


class UniversalFileFactory(AbstractFileFactory):
    """A factory class that instantiates a source file object
    and a target file object for conversion.
    All file types relevant for OpenOffice/LibreOffice import 
    and export are available.
    """

    def __init__(self):
        self.exportSourceFactory = ExportSourceFactory()
        self.exportTargetFactory = ExportTargetFactory()
        self.importObjectsFactory = ImportObjectsFactory()
