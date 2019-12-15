""" Import proofed chapters. 

Read a markdown file with scene text divided by [ChID:x] and [ScID:y] tags 
(as known by yWriter5 RTF proofing export) and replace the scenes
in an yw7 project file.

For further information see https://github.com/peter88213/yWrestler
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import re
import sys
import xml.etree.ElementTree as ET


def format_yw7(text):
    """ Convert markdown to yw7 raw markup. """
    text = text.replace('\n\n', '\n')
    text = text.replace('\[', '[')
    text = text.replace('\]', ']')
    text = re.sub('\*\*(.+?)\*\*', '[b]\g<1>[/b]', text)
    text = re.sub('\*(.+?)\*', '[i]\g<1>[/i]', text)
    return(text)


def md_to_yw7(mdFile, yw7File):
    """ Convert markdown to xml and replace .yw7 file. """
    try:
        with open(mdFile, 'r', encoding='utf-8') as f:
            text = (f.read())
    except(IOError):
        sys.exit(1)

    text = format_yw7(text)
    scenes = {}
    sceneText = ''
    scnID = ''
    lines = text.split('\n')
    for line in lines:
        if line.count('[ChID'):
            pass
        elif line.count('[ScID'):
            scnID = re.search('[0-9]+', line).group()
        elif line.count('[/ChID]'):
            pass
        elif line.count('[/ScID]'):
            scenes[scnID] = sceneText
            sceneText = ''
        else:
            sceneText = sceneText + line + '\n'

    tree = ET.parse(yw7File)
    root = tree.getroot()
    for scn in root.iter('SCENE'):
        scnID = scn.find('ID').text
        scn.find('SceneContent').text = scenes[scnID]
    tree.write(yw7File, encoding='utf-8')


def main():
    """ Call the functions with command line arguments. """
    try:
        mdPath = sys.argv[1]
    except:
        print('Syntax: yw7write.py filename.md')
        sys.exit(1)

    yw7Path = mdPath.split('.md')[0] + '.yw7'
    md_to_yw7(mdPath, yw7Path)


if __name__ == '__main__':
    main()
