"""PyWriter v1.4 - Import and export ywriter7 scenes for proofing. 

Proof reading file format: ODT (OASIS Open Document format) 
with visible chapter and scene tags.
Proofed file format: HTML with visible chapter and scene tags.

Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys
import os

from pywriter.model.odt_proof_writer import OdtProofWriter
from pywriter.model.html_proof_reader import HtmlProofReader
from pywriter.model.yw7file import Yw7File
from pywriter.converter.yw7cnv import Yw7Cnv


def delete_tempfile(filePath):
    if filePath.endswith('.html'):
        try:
            os.remove(filePath)
        except:
            pass


def run(sourcePath):
    sourcePath = sourcePath.replace('file:///', '').replace('%20', ' ')
    converter = Yw7Cnv()

    # The conversion's direction depends on the sourcePath argument.

    if sourcePath.endswith('.yw7'):
        targetDoc = OdtProofWriter(sourcePath.split(
            '.yw7')[0] + '_proof.odt')
        yw7File = Yw7File(sourcePath)
        message = converter.yw7_to_document(yw7File, targetDoc)
        return message

    elif sourcePath.endswith('_proof.html'):
        sourceDoc = HtmlProofReader(sourcePath)
        yw7File = Yw7File(sourcePath.split('_proof.html')[0] + '.yw7')
        message = converter.document_to_yw7(sourceDoc, yw7File)
        delete_tempfile(sourcePath)
        return message

    else:
        delete_tempfile(sourcePath)
        return 'File must be .yw7 or _proof.html type.'


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]

    except:
        files = os.listdir('.')

        for file in files:

            if '.yw7' in file:
                sourcePath = file
                break

        if sourcePath is None:
            print('ERROR: No yWriter 7 project found.')
            exit(1)

    print(run(sourcePath))
