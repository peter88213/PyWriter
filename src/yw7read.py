""" Export chapters for proofing.  
"""

import sys
import xml.etree.ElementTree as ET
import pypandoc


def format_md(text):
    """ Convert yw7 specific markup """
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

    prjText = ''
    for chp in root.iter('CHAPTER'):
        prjText = prjText + '\\[ChID:' + chp.find('ID').text + '\\]\n'
        scnList = chp.find('Scenes')
        for scn in scnList.findall('ScID'):
            scnID = scn.text
            prjText = prjText + '\\[ScID:' + scnID + '\\]\n'
            prjText = prjText + scenes[scnID] + '\n'
            prjText = prjText + '\\[/ScID\\]\n'
        prjText = prjText + '\\[/ChID\\]\n'
    prjText = format_md(prjText)
    return(prjText)


def markdown_to_odt(prjText, odtFile):
    """ run pandoc to create an .odt file """
    pypandoc.convert_text(
        prjText, 'odt', format='markdown_strict', outputfile=odtFile)


def main():
    """ Collect command line arguments and call the functions """
    try:
        yw7Path = sys.argv[1]
        prjText = yw7_to_markdown(yw7Path)
        odtPath = yw7Path.split('.yw7')[0] + '.odt'
        markdown_to_odt(prjText, odtPath)
    except:
        print('Syntax: yw7read.py filename')
        sys.exit(1)


if __name__ == '__main__':
    main()
