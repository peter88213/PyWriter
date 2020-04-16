"""PyWriter v1.4 - Convert yw7 to odt. 

Input file format: yw7
Output file format: odt (with visible or invisible chapter and scene tags) or csv.

Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys

from pywriter.model.odt_proof_writer import OdtProofWriter
from pywriter.model.odt_manuscript_writer import OdtManuscriptWriter
from pywriter.model.odt_scenedesc_writer import OdtSceneDescWriter
from pywriter.model.odt_chapterdesc_writer import OdtChapterDescWriter
from pywriter.model.odt_partdesc_writer import OdtPartDescWriter
from pywriter.model.scenelist import SceneList
from pywriter.plot.plotlist import PlotList
from pywriter.model.odt_file_writer import OdtFileWriter
from pywriter.converter.cnv_runner import CnvRunner


def run(sourcePath, suffix):

    if suffix == '_proof':
        extension = 'odt'
        targetDoc = OdtProofWriter(
            sourcePath.split('.yw7')[0] + suffix + '.odt')

    elif suffix == '_manuscript':
        extension = 'odt'
        targetDoc = OdtManuscriptWriter(
            sourcePath.split('.yw7')[0] + suffix + '.odt')

    elif suffix == '_scenes':
        extension = 'odt'
        targetDoc = OdtSceneDescWriter(
            sourcePath.split('.yw7')[0] + suffix + '.odt')

    elif suffix == '_chapters':
        extension = 'odt'
        targetDoc = OdtChapterDescWriter(
            sourcePath.split('.yw7')[0] + suffix + '.odt')

    elif suffix == '_parts':
        extension = 'odt'
        targetDoc = OdtPartDescWriter(
            sourcePath.split('.yw7')[0] + suffix + '.odt')

    elif suffix == '_scenelist':
        extension = 'csv'
        targetDoc = SceneList(sourcePath.split('.yw7')[0] + suffix + '.csv')

    elif suffix == '_plotlist':
        extension = 'csv'
        targetDoc = PlotList(sourcePath.split('.yw7')[0] + suffix + '.csv')

    else:
        extension = 'odt'
        targetDoc = OdtFileWriter(sourcePath.split('.yw7')[0] + '.odt')

    converter = CnvRunner(sourcePath, targetDoc,
                          extension, False, suffix)


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
