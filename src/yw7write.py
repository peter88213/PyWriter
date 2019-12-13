""" Import proofed chapters. 
"""
import re
import sys
import xml.etree.ElementTree as ET


def read_md(mdFile):
    """ Read markdown from .md file. """
    with open(mdFile, 'r') as f:
        mdText = f.read()
    return(mdText)


def format_yw7(text):
    """ Convert into yw7 raw markup """
    text = text.replace('\n\n', '\n')
    text = text.replace('\[', '[')
    text = text.replace('\]', ']')
    text = re.sub('\*\*(.+?)\*\*', '[b]\g<1>[/b]', text)
    text = re.sub('\*(.+?)\*', '[i]\g<1>[/i]', text)
    return(text)


def markdown_to_yw7(prjText, yw7File):
    """ Convert markdown to xml and replace .yw7 file. """
    prjText = format_yw7(prjText)
    prjObj = parse_yw7(prjText)
    tree = ET.parse(yw7File)
    root = tree.getroot()  # all item attributes
    return()


def parse_yw7(rawText):
    """ Part yw7 raw text into chapters and scenes. """
    project = {}
    chapters = {}
    scenes = {}
    sceneList = []
    sceneText = ''
    chpID = 0
    scnID = 0
    projectData = rawText.split('\n')
    for line in projectData:
        if line.count('[ChID'):
            chpID = re.search('[0-9]+', line).group()
        elif line.count('[ScID'):
            scnID = re.search('[0-9]+', line).group()
            sceneList.append(scnID)
        elif line.count('[/ChID]'):
            chapters[chpID] = sceneList
            sceneList = []
        elif line.count('[/ScID]'):
            scenes[scnID] = sceneText
            sceneText = ''
        else:
            sceneText = sceneText + line + '\n'
    project['scenes'] = scenes
    project['chapters'] = chapters
    return(project)


def main():
    """ Call the functions with command line arguments. """
    try:
        mdPath = sys.argv[1]
    except:
        print('Syntax: yw7write.py filename.md')
        sys.exit(1)

    prjText = read_md(mdPath)
    # Read markdown from .md file.
    yw7Path = mdPath.split('.md')[0] + '.yw7'
    markdown_to_yw7(prjText, yw7Path)
    # Convert markdown to xml and replace .yw7 file.


if __name__ == '__main__':
    main()
