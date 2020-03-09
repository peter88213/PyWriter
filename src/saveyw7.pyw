"""PyWriter v1.4 - Convert html to yw7. 

Input file format: html (with visible or invisible chapter and scene tags).

Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys
import os

from pywriter.model.html_proof_reader import HtmlProofReader
from pywriter.model.html_manuscript_reader import HtmlManuscriptReader
from pywriter.model.html_scenedesc_reader import HtmlSceneDescReader
from pywriter.model.html_chapterdesc_reader import HtmlChapterDescReader
from pywriter.model.scenelist import SceneList
from pywriter.plot.plotlist import PlotList
from pywriter.converter.cnv_runner import CnvRunner


class Converter(CnvRunner):
    """Deletes temporary html or csv file after conversion. """

    def convert(self, sourcePath,
                document,
                extension,
                suffix):

        CnvRunner.convert(self, sourcePath,
                          document,
                          extension,
                          suffix)

        if sourcePath.endswith('.html'):

            if os.path.isfile(sourcePath.split('.html')[0] + '.odt'):
                try:
                    os.remove(sourcePath)
                except:
                    pass

        elif sourcePath.endswith('.csv'):

            if os.path.isfile(sourcePath.split('.csv')[0] + '.ods'):
                try:
                    os.remove(sourcePath)
                except:
                    pass


def run(sourcePath):
    sourcePath = sourcePath.replace('file:///', '').replace('%20', ' ')

    if sourcePath.endswith('_proof.html'):
        suffix = '_proof'
        extension = 'html'
        sourceDoc = HtmlProofReader(sourcePath)

    elif sourcePath.endswith('_manuscript.html'):
        suffix = '_manuscript'
        extension = 'html'
        sourceDoc = HtmlManuscriptReader(sourcePath)

    elif sourcePath.endswith('_scenes.html'):
        suffix = '_scenes'
        extension = 'html'
        sourceDoc = HtmlSceneDescReader(sourcePath)

    elif sourcePath.endswith('_chapters.html'):
        suffix = '_chapters'
        extension = 'html'
        sourceDoc = HtmlChapterDescReader(sourcePath)

    elif sourcePath.endswith('_parts.html'):
        suffix = '_parts'
        extension = 'html'
        sourceDoc = HtmlChapterDescReader(sourcePath)

    elif sourcePath.endswith('_scenelist.csv'):
        suffix = '_scenelist'
        extension = 'csv'
        sourceDoc = SceneList(sourcePath)

    elif sourcePath.endswith('_plotlist.csv'):
        suffix = '_plotlist'
        extension = 'csv'
        sourceDoc = PlotList(sourcePath)

    else:
        suffix = ''
        extension = ''
        sourceDoc = None

    converter = Converter(sourcePath, sourceDoc,
                          extension, False, suffix)


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]
    except:
        sourcePath = ''

    run(sourcePath)
