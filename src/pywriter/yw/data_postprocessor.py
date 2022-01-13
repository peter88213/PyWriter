"""Provide a strategy class to postprocess utf-8 encoded yWriter XML data files.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
from pywriter.yw.utf8_postprocessor import Utf8Postprocessor


class DataPostprocessor(Utf8Postprocessor):
    """Postprocess utf-8 encoded yWriter data."""

    def postprocess_xml_file(self, filePath):
        '''Postprocess the xml files created by ElementTree:
        Put headers on top, insert the missing CDATA tags,
        and replace xml entities by plain text.
        Return a message beginning with SUCCESS or ERROR.
        '''

        path, extension = os.path.splitext(filePath)

        characterPath = path + '_Characters.xml'
        message = super().postprocess_xml_file(characterPath)

        if message.startswith('ERROR'):
            return message

        locationPath = path + '_Locations.xml'
        message = super().postprocess_xml_file(locationPath)

        if message.startswith('ERROR'):
            return message

        itemPath = path + '_Items.xml'
        message = super().postprocess_xml_file(itemPath)

        if message.startswith('ERROR'):
            return message

        return 'SUCCESS: All XML data files written.'
