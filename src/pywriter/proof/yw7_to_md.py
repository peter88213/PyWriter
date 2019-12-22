""" PyWriter module

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.project import PywProject

HEADING_MARKER = ("##", "#")


def yw7_to_md(yw7File, mdFile):
    """ Read .yw7 file and convert xml to markdown. """

    def format_chapter_title(text):
        """ Fix auto-chapter titles for non-English """
        text = text.replace('Chapter ', '')
        return(text)

    def format_md(text):
        """ Convert yw7 specific markup """
        text = text.replace('\n\n', '\n')
        text = text.replace('\n', '\n\n')
        text = text.replace('*', '\*')
        text = text.replace('[i]', '*')
        text = text.replace('[/i]', '*')
        text = text.replace('[b]', '**')
        text = text.replace('[/b]', '**')
        return(text)

    prj = PywProject(yw7File)
    prjText = ''
    for chID in prj.sceneLists:
        prjText = prjText + '\\[ChID:' + chID + '\\]\n'
        headingMarker = HEADING_MARKER[prj.chapterTypes[chID]]
        prjText = prjText + headingMarker + \
            format_chapter_title(prj.chapterTitles[chID]) + '\n'
        for scID in prj.sceneLists[chID]:
            prjText = prjText + '\\[ScID:' + scID + '\\]\n'
            try:
                prjText = prjText + prj.sceneContents[scID] + '\n'
            except(TypeError):
                prjText = prjText + '\n'
            prjText = prjText + '\\[/ScID\\]\n'
        prjText = prjText + '\\[/ChID\\]\n'
    prjText = format_md(prjText)

    with open(mdFile, 'w', encoding='utf-8') as f:
        f.write(prjText)

    return('\nSUCCESS: ' + str(len(prj.sceneContents)) + ' Scenes written to "' + mdFile + '".')


if __name__ == '__main__':
    pass
