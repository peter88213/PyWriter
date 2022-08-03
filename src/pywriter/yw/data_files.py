"""Provide a class for yWriter XML data files.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import xml.etree.ElementTree as ET
from pywriter.pywriter_globals import *
from pywriter.yw.yw7_file import Yw7File


class DataFiles(Yw7File):
    """yWriter XML data files representation.

    Public methods: 
        merge(source) -- Update instance variables from a source instance.
        
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
        Return a message beginning with the ERROR constant in case of error.
        """
        path, __ = os.path.splitext(ywProject.filePath)
        characterPath = f'{path}_Characters.xml'
        characterSubtree = ywProject.tree.find('CHARACTERS')
        characterTree = ET.ElementTree(characterSubtree)
        try:
            characterTree.write(characterPath, xml_declaration=False, encoding='utf-8')
        except(PermissionError):
            return f'{ERROR}{_("File is write protected")}: "{os.path.normpath(characterPath)}".'

        locationPath = f'{path}_Locations.xml'
        locationSubtree = ywProject.tree.find('LOCATIONS')
        locationTree = ET.ElementTree(locationSubtree)
        try:
            locationTree.write(locationPath, xml_declaration=False, encoding='utf-8')
        except(PermissionError):
            return f'{ERROR}{_("File is write protected")}: "{os.path.normpath(locationPath)}".'

        itemPath = f'{path}_Items.xml'
        itemSubtree = ywProject.tree.find('ITEMS')
        itemTree = ET.ElementTree(itemSubtree)
        try:
            itemTree.write(itemPath, xml_declaration=False, encoding='utf-8')
        except(PermissionError):
            return f'{ERROR}{_("File is write protected")}: "{os.path.normpath(itemPath)}".'

        return 'All XML data files written.'

    def _postprocess_xml_file(self, filePath):
        '''Postprocess three xml files created by ElementTree.
        
        Positional argument:
            filePath -- str: path to .yw7 xml file.
            
        Generate the xml file paths from the .yw7 path. 
        Read, postprocess and write the characters, locations, and items xml files.        
        Return a message beginning with the ERROR constant in case of error.
        Extends the superclass method.
        '''
        path, __ = os.path.splitext(filePath)
        characterPath = f'{path}_Characters.xml'
        message = super()._postprocess_xml_file(characterPath)
        if message.startswith(ERROR):
            return message

        locationPath = f'{path}_Locations.xml'
        message = super()._postprocess_xml_file(locationPath)
        if message.startswith(ERROR):
            return message

        itemPath = f'{path}_Items.xml'
        message = super()._postprocess_xml_file(itemPath)
        if message.startswith(ERROR):
            return message

        return 'All XML data files written.'

    def merge(self, source):
        """Update instance variables from a source instance.
        
        Positional arguments:
            source -- Novel subclass instance to merge.
        
        Return a message beginning with the ERROR constant in case of error.
        Overrides the superclass method.
        """
        self.characters = source.characters
        self.srtCharacters = source.srtCharacters
        self.locations = source.locations
        self.srtLocations = source.srtLocations
        self.items = source.items
        self.srtItems = source.srtItems
        return 'XML Data file content updated from novel.'
