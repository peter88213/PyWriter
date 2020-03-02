"""PyWriter v1.3 - Convert html to yw7. 

Input file format: html (with visible or invisible chapter and scene tags).

Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys
import os

from pywriter.model.html_proof import HtmlProof
from pywriter.model.html_manuscript import HtmlManuscript
from pywriter.model.html_scenedesc import HtmlSceneDesc
from pywriter.model.html_chapterdesc import HtmlChapterDesc
from pywriter.model.html_partdesc import HtmlPartDesc
from pywriter.model.yw7file import Yw7File
from pywriter.converter.yw7cnv import Yw7Cnv
from pywriter.model.scenelist import SceneList
from pywriter.plot.plotlist import PlotList


def delete_tempfile(filePath):

    if filePath.endswith('.html'):

        if os.path.isfile(filePath.split('.html')[0] + '.odt'):
            try:
                os.remove(filePath)
            except:
                pass

    elif filePath.endswith('.csv'):

        if os.path.isfile(filePath.split('.csv')[0] + '.ods'):
            try:
                os.remove(filePath)
            except:
                pass


def run(sourcePath):
    sourcePath = sourcePath.replace('file:///', '').replace('%20', ' ')

    if sourcePath.endswith('_proof.html'):
        yw7File = Yw7File(sourcePath.split('_proof.html')[0] + '.yw7')
        sourceDoc = HtmlProof(sourcePath)

    elif sourcePath.endswith('_manuscript.html'):
        yw7File = Yw7File(sourcePath.split('_manuscript.html')[0] + '.yw7')
        sourceDoc = HtmlManuscript(sourcePath)

    elif sourcePath.endswith('_scenes.html'):
        yw7File = Yw7File(sourcePath.split('_scenes.html')[0] + '.yw7')
        sourceDoc = HtmlSceneDesc(sourcePath)

    elif sourcePath.endswith('_chapters.html'):
        yw7File = Yw7File(sourcePath.split('_chapters.html')[0] + '.yw7')
        sourceDoc = HtmlChapterDesc(sourcePath)

    elif sourcePath.endswith('_parts.html'):
        yw7File = Yw7File(sourcePath.split('_parts.html')[0] + '.yw7')
        sourceDoc = HtmlPartDesc(sourcePath)

    elif sourcePath.endswith('_scenelist.csv'):
        yw7File = Yw7File(sourcePath.split('_scenes.csv')[0] + '.yw7')
        sourceDoc = SceneList(sourcePath)

    elif sourcePath.endswith('_plotlist.csv'):
        yw7File = Yw7File(sourcePath.split('_plot.csv')[0] + '.yw7')
        sourceDoc = PlotList(sourcePath)

    else:
        return 'ERROR: File format not supported.'

    converter = Yw7Cnv()
    message = converter.document_to_yw7(sourceDoc, yw7File)

    if not message.startswith('ERROR'):
        delete_tempfile(sourcePath)

    return message


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]
    except:
        sourcePath = ''
    print(run(sourcePath))
