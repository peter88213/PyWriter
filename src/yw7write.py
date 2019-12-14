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

# Transfer data for document parsing
CHAPTERS = {}
SCENES = {}


def read_file(inputFile):
    with open(inputFile, 'r') as f:
        return(f.read())


def write_yw7(text, yw7File):
    """ Convert markdown to xml and replace .yw7 file. """

    def format_yw7(text):
        """ Convert markdown to yw7 raw markup. """
        text = text.replace('\n\n', '\n')
        text = text.replace('\[', '[')
        text = text.replace('\]', ']')
        text = re.sub('\*\*(.+?)\*\*', '[b]\g<1>[/b]', text)
        text = re.sub('\*(.+?)\*', '[i]\g<1>[/i]', text)
        return(text)

    def convert_markdown(text):
        """ Convert markdown into yw7 chapters and scenes. """
        global CHAPTERS, SCENES
        text = format_yw7(text)
        sceneList = []
        sceneText = ''
        chpID = 0
        scnID = 0
        projectData = text.split('\n')
        for line in projectData:
            if line.count('[ChID'):
                chpID = re.search('[0-9]+', line).group()
            elif line.count('[ScID'):
                scnID = re.search('[0-9]+', line).group()
                sceneList.append(scnID)
            elif line.count('[/ChID]'):
                CHAPTERS[chpID] = sceneList
                sceneList = []
            elif line.count('[/ScID]'):
                SCENES[scnID] = sceneText
                sceneText = ''
            else:
                sceneText = sceneText + line + '\n'

    convert_markdown(text)
    tree = ET.parse(yw7File)
    root = tree.getroot()  # all item attributes


def main():
    """ Call the functions with command line arguments. """
    try:
        mdPath = sys.argv[1]
    except:
        print('Syntax: yw7write.py filename.md')
        sys.exit(1)

    prjText = read_file(mdPath)
    # Read document from markdown file.

    yw7Path = mdPath.split('.md')[0] + '.yw7'
    write_yw7(prjText, yw7Path)
    # Convert markdown to xml and modify .yw7 file.

    for scene in SCENES.values():
        print(scene)
    for chapter in CHAPTERS.values():
        print(chapter)


if __name__ == '__main__':
    main()
