""" Import proofed chapters. 
"""
import re
import sys
import xml.etree.ElementTree as ET
import pypandoc


def format_md(text):
    """ Beautify pandoc-generated md """
    text = text.replace('\r', '\n')
    text = text.replace('\n\n', '\n')
    text = text.replace('\n\n', '\n')
    text = text.replace('\n', '\n\n')
    return(text)


def format_yw7(text):
    """ Convert into yw7 raw markup """
    text = text.replace('\n\n', '\n')
    text = text.replace('\[', '[')
    text = text.replace('\]', ']')
    text = re.sub('\*\*(.+?)\*\*', '[b]\g<1>[/b]', text)
    text = re.sub('\*(.+?)\*', '[i]\g<1>[/i]', text)
    return(text)


def parse_yw7(rawText):
    """ Part yw7 raw text into chapters and scenes """
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


def odt_to_markdown(odtFile):
    """ run pandoc to create a markdown string """
    mdText = pypandoc.convert_file(
        odtFile, 'markdown_strict', format='odt', extra_args=['--wrap=none'])
    mdText = format_md(mdText)
    return(mdText)


def write_markdown(mdText, mdFile):
    with open(mdFile, 'w') as f:
        f.write(mdText)


def markdown_to_yw7(prjText, yw7File):
    prjText = format_yw7(prjText)
    prjObj = parse_yw7(prjText)
    tree = ET.parse(yw7File)
    root = tree.getroot()  # all item attributes
    return()


def main():
    """ Collect command line arguments, call conversion and generate string. """
    try:
        odtPath = sys.argv[1]
        mdText = odt_to_markdown(odtPath)
    except:
        print('Syntax: yw7write.py filename')
        sys.exit(1)

    mdPath = odtPath.split('.odt')[0] + '.md'
    write_markdown(mdText, mdPath)

    yw7Path = odtPath.split('.odt')[0] + '.yw7'
    markdown_to_yw7(mdText, yw7Path)


if __name__ == '__main__':
    main()
