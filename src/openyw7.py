"""PyWriter v1.3 - Convert yw7 to odt. 

Input file format: yw7
Output file format: odt (with visible or invisible chapter and scene tags) or csv.

Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys

from pywriter.model.odt_proof import OdtProof
from pywriter.model.odt_manuscript import OdtManuscript
from pywriter.model.odt_scenedesc import OdtSceneDesc
from pywriter.model.odt_chapterdesc import OdtChapterDesc
from pywriter.model.odt_partdesc import OdtPartDesc
from pywriter.model.yw7file import Yw7File
from pywriter.converter.yw7cnv import Yw7Cnv
from pywriter.model.scenelist import SceneList
from pywriter.plot.plotlist import PlotList


def run(sourcePath, suffix):

    if suffix == '_proof':
        yw7File = Yw7File(sourcePath)
        targetDoc = OdtProof(sourcePath.split('.yw7')[0] + suffix + '.odt')

    elif suffix == '_manuscript':
        yw7File = Yw7File(sourcePath)
        targetDoc = OdtManuscript(
            sourcePath.split('.yw7')[0] + suffix + '.odt')

    elif suffix == '_scenes':
        yw7File = Yw7File(sourcePath)
        targetDoc = OdtSceneDesc(sourcePath.split('.yw7')[0] + suffix + '.odt')

    elif suffix == '_chapters':
        yw7File = Yw7File(sourcePath)
        targetDoc = OdtChapterDesc(
            sourcePath.split('.yw7')[0] + suffix + '.odt')

    elif suffix == '_parts':
        yw7File = Yw7File(sourcePath)
        targetDoc = OdtPartDesc(sourcePath.split('.yw7')[0] + suffix + '.odt')

    elif suffix == '_scenelist':
        yw7File = Yw7File(sourcePath)
        targetDoc = SceneList(sourcePath.split('.yw7')[0] + suffix + '.csv')

    elif suffix == '_plotlist':
        yw7File = Yw7File(sourcePath)
        targetDoc = PlotList(sourcePath.split('.yw7')[0] + suffix + '.csv')

    else:
        return 'ERROR: Target file format not supported.'

    converter = Yw7Cnv()
    message = converter.yw7_to_document(yw7File, targetDoc)

    return message


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]
    except:
        sourcePath = ''

    if sourcePath.endswith('.yw7'):
        try:
            suffix = sys.argv[2]
        except:
            suffix = ''

        print(run(sourcePath, suffix))

    else:
        print('ERROR: File is not an yWriter 7 project.')
