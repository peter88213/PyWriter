"""Provide a class for yWriter XML data files.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import xml.etree.ElementTree as ET

from pywriter.pywriter_globals import ERROR
from pywriter.yw.yw7_file import Yw7File


class DataFiles(Yw7File):
    """yWriter XML data files representation.

    Public methods: 
        merge(novel) -- Copy required attributes of the novel object.    
    """

    DESCRIPTION = 'yWriter XML data files'
    EXTENSION = '.xml'

    def _write_element_tree(self, ywProject):
        """Write back the xml element tree to a yWriter xml file located at filePath.
        Return a message beginning with the ERROR constant in case of error.
        """

        path, __ = os.path.splitext(ywProject.filePath)

        characterPath = f'{path}_Characters.xml'
        characterSubtree = ywProject.tree.find('CHARACTERS')
        characterTree = ET.ElementTree(characterSubtree)

        try:
            characterTree.write(characterPath, xml_declaration=False, encoding='utf-8')

        except(PermissionError):
            return f'{ERROR}"{os.path.normpath(characterPath)}" is write protected.'

        locationPath = f'{path}_Locations.xml'
        locationSubtree = ywProject.tree.find('LOCATIONS')
        locationTree = ET.ElementTree(locationSubtree)

        try:
            locationTree.write(locationPath, xml_declaration=False, encoding='utf-8')

        except(PermissionError):
            return f'{ERROR}"{os.path.normpath(locationPath)}" is write protected.'

        itemPath = f'{path}_Items.xml'
        itemSubtree = ywProject.tree.find('ITEMS')
        itemTree = ET.ElementTree(itemSubtree)

        try:
            itemTree.write(itemPath, xml_declaration=False, encoding='utf-8')

        except(PermissionError):
            return f'{ERROR}"{os.path.normpath(itemPath)}" is write protected.'

        return 'All XML data files written.'

    def _postprocess_xml_file(self, filePath):
        '''Postprocess the xml files created by ElementTree:
        Put headers on top, insert the missing CDATA tags,
        and replace xml entities by plain text.
        Return a message beginning with the ERROR constant in case of error.
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
        """Copy required attributes of the source object.
        Return a message beginning with the ERROR constant in case of error.
        Override the superclass method.
        """
        self.characters = source.characters
        self.srtCharacters = source.srtCharacters
        self.locations = source.locations
        self.srtLocations = source.srtLocations
        self.items = source.items
        self.srtItems = source.srtItems
        return 'XML Data file content updated from novel.'
