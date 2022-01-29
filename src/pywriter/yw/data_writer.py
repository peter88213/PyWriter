"""Provide a strategy class to write utf-8 encoded yWriter XML data files.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import xml.etree.ElementTree as ET


class DataWriter():
    """Write utf-8 encoded yWriter XML data files.

    Public methods: 
        write_element_tree(ywProject) -- Write back the xml element tree to a a yWriter xml file.   
    """

    def write_element_tree(self, ywProject):
        """Write back the xml element tree to a yWriter xml file located at filePath.
        Return a message beginning with SUCCESS or ERROR.
        """

        path, extension = os.path.splitext(ywProject.filePath)

        characterPath = f'{path}_Characters.xml'
        characterSubtree = ywProject.tree.find('CHARACTERS')
        characterTree = ET.ElementTree(characterSubtree)

        try:
            characterTree.write(characterPath, xml_declaration=False, encoding='utf-8')

        except(PermissionError):
            return f'ERROR: "{os.path.normpath(characterPath)}" is write protected.'

        locationPath = f'{path}_Locations.xml'
        locationSubtree = ywProject.tree.find('LOCATIONS')
        locationTree = ET.ElementTree(locationSubtree)

        try:
            locationTree.write(locationPath, xml_declaration=False, encoding='utf-8')

        except(PermissionError):
            return f'ERROR: "{os.path.normpath(locationPath)}" is write protected.'

        itemPath = f'{path}_Items.xml'
        itemSubtree = ywProject.tree.find('ITEMS')
        itemTree = ET.ElementTree(itemSubtree)

        try:
            itemTree.write(itemPath, xml_declaration=False, encoding='utf-8')

        except(PermissionError):
            return f'ERROR: "{os.path.normpath(itemPath)}" is write protected.'

        return 'SUCCESS'
