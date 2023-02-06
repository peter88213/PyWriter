"""Provide a class for yWriter XML data files.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import xml.etree.ElementTree as ET
from pywriter.pywriter_globals import *
from pywriter.yw.yw7_file import Yw7File


class DataFiles(Yw7File):
    """yWriter XML data files representation.
       
    yWriter can import or export characters, locations and items as separate
    xml files. This class represents a set of three xml files generated from
    a yWriter 7 project.
    """
    DESCRIPTION = _('yWriter XML data files')
    EXTENSION = '.xml'

    def _write_element_tree(self, ywProject):
        """Save the characters/locations/items subtrees as separate xml files
        
        Positional argument:
            ywProject -- Yw7File instance.
            
        Extract the characters/locations/items xml subtrees from a yWriter project.
        Generate the xml file paths from the .yw7 path and write each subtree to an xml file.
        Raise the "Error" exception in case of error. 
        """
        path, __ = os.path.splitext(ywProject.filePath)
        characterPath = f'{path}_Characters.xml'
        characterSubtree = ywProject.tree.find('CHARACTERS')
        characterTree = ET.ElementTree(characterSubtree)
        try:
            characterTree.write(characterPath, xml_declaration=False, encoding='utf-8')
        except(PermissionError):
            raise Error(f'{_("File is write protected")}: "{norm_path(characterPath)}".')

        locationPath = f'{path}_Locations.xml'
        locationSubtree = ywProject.tree.find('LOCATIONS')
        locationTree = ET.ElementTree(locationSubtree)
        try:
            locationTree.write(locationPath, xml_declaration=False, encoding='utf-8')
        except(PermissionError):
            raise Error(f'{_("File is write protected")}: "{norm_path(locationPath)}".')

        itemPath = f'{path}_Items.xml'
        itemSubtree = ywProject.tree.find('ITEMS')
        itemTree = ET.ElementTree(itemSubtree)
        try:
            itemTree.write(itemPath, xml_declaration=False, encoding='utf-8')
        except(PermissionError):
            raise Error(f'{_("File is write protected")}: "{norm_path(itemPath)}".')

    def _postprocess_xml_file(self, filePath):
        '''Postprocess three xml files created by ElementTree.
        
        Positional argument:
            filePath -- str: path to .yw7 xml file.
            
        Generate the xml file paths from the .yw7 path. 
        Read, postprocess and write the characters, locations, and items xml files.        
        Extends the superclass method.
        '''
        path, __ = os.path.splitext(filePath)
        characterPath = f'{path}_Characters.xml'
        super()._postprocess_xml_file(characterPath)
        locationPath = f'{path}_Locations.xml'
        super()._postprocess_xml_file(locationPath)
        itemPath = f'{path}_Items.xml'
        super()._postprocess_xml_file(itemPath)

