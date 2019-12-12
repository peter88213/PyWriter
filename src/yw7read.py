'''
Created on 12.12.2019

@author: Peter
'''
import xml.etree.ElementTree as ET


def format_md(text):
    text = text.replace('\n\n', '\n')
    text = text.replace('\n', '\n\n')
    text = text.replace('[i]', '*')
    text = text.replace('[/i]', '*')
    text = text.replace('[b]', '**')
    text = text.replace('[/b]', '**')
    return(text)


def read_xml(yw7File):
    tree = ET.parse(yw7File)
    root = tree.getroot()  # all item attributes

    scenes = {}
    for scn in root.iter('SCENE'):
        scnID = scn.find('ID').text
        scenes[scnID] = scn.find('SceneContent').text

    chapters = {}
    for chp in root.iter('CHAPTER'):
        chpNr = int(chp.find('SortOrder').text)
        print('chapter Nr: ', chpNr)
        chpContent = ''
        chpID = chp.find('ID').text
        print('chapter ID: ', chpID)
        chpContent = chpContent + '\\[ChID:' + chpID + '\\]\n'
        scnList = chp.find('Scenes')
        for scn in scnList.findall('ScID'):
            scnID = scn.text
            print('sceneID: ' + scnID)
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
    print(prjText)
    with open('out.md', 'w') as f:
        f.write(prjText)
    return(prjText)


if __name__ == '__main__':
    pass
