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

    mdPrj = PywProject()
    sceneText = ''
    scID = ''
    chID = ''
    inScene = False

    lines = text.split('\n')
    for line in lines:
        if line.count('[ScID'):
            scID = re.search('[0-9]+', line).group()
            mdPrj.scenes[scID] = PywProject.Scene()
            mdPrj.chapters[chID].scenes.append(scID)
            inScene = True
        elif line.count('[/ScID]'):
            mdPrj.scenes[scID].sceneContent = sceneText
            sceneText = ''
            inScene = False
        elif line.count('[ChID'):
            chID = re.search('[0-9]+', line).group()
            mdPrj.chapters[chID] = PywProject.Chapter()
        elif line.count('[/ChID]'):
            pass
        elif inScene:
            sceneText = sceneText + line + '\n'

    ywPrj = PywProject()
    ywPrj.read(yw7File)

    for scID in mdPrj.scenes:
        ywPrj.scenes[scID].sceneContent = mdPrj.scenes[scID].sceneContent

    return(ywPrj.write(yw7File))


if __name__ == '__main__':
    pass
