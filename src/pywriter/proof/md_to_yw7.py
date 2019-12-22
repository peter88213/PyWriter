""" PyWriter module

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import re
from pywriter.project import PywProject


def format_chapter_title(text):
    """ Fix auto-chapter titles for non-English """
    text = text.replace('Chapter ', '')
    return(text)


def md_to_yw7(mdFile, yw7File):
    """ Convert markdown to xml and replace .yw7 file. """

    def format_yw7(text):
        """ Convert markdown to yw7 raw markup. """
        text = text.replace('\r', '\n')
        text = text.replace('\n\n', '\n')
        text = text.replace('\[', '[')
        text = text.replace('\]', ']')
        text = text.replace('\\*', '_asterisk_')
        text = re.sub('\*\*(.+?)\*\*', '[b]\g<1>[/b]', text)
        text = re.sub('\*(.+?)\*', '[i]\g<1>[/i]', text)
        text = text.replace('_asterisk_', '*')
        return(text)

    try:
        with open(mdFile, 'r', encoding='utf-8') as f:
            text = (f.read())
    except(FileNotFoundError):
        return('\nERROR: "' + mdFile + '" not found.')

    text = format_yw7(text)
    sceneContents = {}
    sceneText = ''
    scID = ''
    inScene = False
    lines = text.split('\n')
    for line in lines:
        if line.count('[ChID'):
            pass
        elif line.count('[ScID'):
            scID = re.search('[0-9]+', line).group()
            inScene = True
        elif line.count('[/ChID]'):
            pass
        elif line.count('[/ScID]'):
            sceneContents[scID] = sceneText
            sceneText = ''
            inScene = False
        elif inScene:
            sceneText = sceneText + line + '\n'

    prj = PywProject(yw7File)

    return(prj.write_scene_contents(sceneContents))


if __name__ == '__main__':
    pass
