""" Export chapters for proofing.

    Read yWriter7 project file and create a Markdown file 
    with scene text divided by [ChID:x] and [ScID:y] tags
    as known by yWriter5 RTF proofing export.
"""
import sys
import xml.etree.ElementTree as ET


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
    """ Read .yw7 file and convert xml to markdown. """
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


def write_md(mdText, mdPath):
    """ Write markdown to .md file. """
    with open(mdPath, 'w') as f:
        f.write(mdText)


def main():
    """ Call the functions with command line arguments. """
    try:
        yw7Path = sys.argv[1]
    except:
        print('Syntax: yw7read.py filename.yw7')
        sys.exit(1)

    prjText = yw7_to_markdown(yw7Path)
    # Read .yw7 file and convert xml to markdown.
    mdPath = yw7Path.split('.yw7')[0] + '.md'
    write_md(prjText, mdPath)
    # Write markdown to .md file.


if __name__ == '__main__':
    main()
