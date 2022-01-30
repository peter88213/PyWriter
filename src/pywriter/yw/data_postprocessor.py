"""Provide a strategy class to postprocess utf-8 encoded yWriter XML data files.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os

from pywriter.pywriter_globals import ERROR
from pywriter.yw.yw7_postprocessor import Yw7Postprocessor


class DataPostprocessor(Yw7Postprocessor):
    """Postprocess utf-8 encoded yWriter data.

    Public methods: 
        postprocess_xml_file(filePath) -- Postprocess the xml files created by ElementTree.    
    """

    def postprocess_xml_file(self, filePath):
        '''Postprocess the xml files created by ElementTree:
        Put headers on top, insert the missing CDATA tags,
        and replace xml entities by plain text.
        Return a message beginning with SUCCESS or ERROR.
        '''

        path, extension = os.path.splitext(filePath)

        characterPath = f'{path}_Characters.xml'
        message = super().postprocess_xml_file(characterPath)

        if message.startswith(ERROR):
            return message

        locationPath = f'{path}_Locations.xml'
        message = super().postprocess_xml_file(locationPath)

        if message.startswith(ERROR):
            return message

        itemPath = f'{path}_Items.xml'
        message = super().postprocess_xml_file(itemPath)

        if message.startswith(ERROR):
            return message

        return 'SUCCESS: All XML data files written.'
