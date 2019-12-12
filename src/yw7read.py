""" Read an .yw7 project file and create .odt for proof reading.  
"""

import sys
import xml.etree.ElementTree as ET
import pypandoc


def format_md(text):
    text = text.replace('\n\n', '\n')
    text = text.replace('\n', '\n\n')
    text = text.replace('[i]', '*')
    text = text.replace('[/i]', '*')
    text = text.replace('[b]', '**')
    text = text.replace('[/b]', '**')
    return(text)


def yw7_to_markdown(yw7File):
    """ Convert .yw7 format into markdown_strict. """
    tree = ET.parse(yw7File)
    root = tree.getroot()  # all item attributes

    scenes = {}
    for scn in root.iter('SCENE'):
        scnID = scn.find('ID').text
        scenes[scnID] = scn.find('SceneContent').text

    chapters = {}
    for chp in root.iter('CHAPTER'):
        chpNr = int(chp.find('SortOrder').text)
        chpContent = ''
        chpID = chp.find('ID').text
        chpContent = chpContent + '\\[ChID:' + chpID + '\\]\n'
        scnList = chp.find('Scenes')
        for scn in scnList.findall('ScID'):
            scnID = scn.text
            chpContent = chpContent + '\\[ScID:' + scnID + '\\]\n'
            chpContent = chpContent + scenes[scnID] + '\n'
            chpContent = chpContent + '\\[/ScID\\]\n'
        chpContent = chpContent + '\\[/ChID\\]\n'
        chapters[chpNr] = chpContent

    prjText = ''
    chpNr = 1
    while chpNr <= len(chapters):
        prjText = prjText + chapters[chpNr]
        chpNr = chpNr + 1
    prjText = format_md(prjText)
    return(prjText)


def main():
    """ Collect command line arguments, call conversion and generate .odt. """
    try:
        yw7Path = sys.argv[1]
        prjText = yw7_to_markdown(yw7Path)
        odtPath = yw7Path.split('.yw7')[0] + '.odt'
        pypandoc.convert_text(
            prjText, 'odt', format='markdown_strict', outputfile=odtPath)
    except:
        print('Syntax: yw7read.py filename')
        sys.exit(1)


if __name__ == '__main__':
    main()
