""" Import proofed chapters. 

Read a html file divided into ChID:x and ScID:y sections 
and replace the scenes in an yw7 project file.

For further information see https://github.com/peter88213/yWrestler
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys
import re
from html.parser import HTMLParser
import xml.etree.ElementTree as ET

# Transfer data for document parsing
CHAPTERS = {}
SCENES = {}

# States of document parsing
S_NONE = 0
S_CHAPTER = 1
S_SCENE = 2


def read_file(inputFile):
    with open(inputFile, 'r') as f:
        return(f.read())


def write_yw7(text, yw7File):
    """ Modify .yw7 file. """

    def format_yw7(text):
        """ Convert html markup to yw7 raw markup """
        text = text.replace('<i>', '[i]')
        text = text.replace('</i>', '[/i]')
        text = text.replace('<I>', '[i]')
        text = text.replace('</I>', '[/i]')
        text = text.replace('<em>', '[i]')
        text = text.replace('</em>', '[/i]')
        text = text.replace('<EM>', '[i]')
        text = text.replace('</EM>', '[/i]')
        text = text.replace('<b>', '[b]')
        text = text.replace('</b>', '[/b]')
        text = text.replace('<B>', '[b]')
        text = text.replace('</B>', '[/b]')
        text = text.replace('<strong>', '[b]')
        text = text.replace('</strong>', '[/b]')
        text = text.replace('<STRONG>', '[b]')
        text = text.replace('</STRONG>', '[/b]')
        text = text.replace('\n', '')
        text = text.replace('\t', ' ')
        while text.count('  '):
            text = text.replace('  ', ' ')
        return(text)

    class MyHTMLParser(HTMLParser):
        """ State machine generating global data """
        sceneList = []
        sceneText = ''
        chpID = 0
        scnID = 0
        docState = S_NONE

        def handle_starttag(self, tag, attrs):
            if tag == 'div':
                if attrs[0][0] == 'id':
                    if attrs[0][1].count('ChID') == 1:
                        self.docState = S_CHAPTER
                        self.chpID = re.search('[0-9]+', attrs[0][1]).group()
                        #print('[ChID:' + self.chpID + ']')
                    elif attrs[0][1].count('ScID') == 1:
                        self.docState = S_SCENE
                        self.scnID = re.search('[0-9]+', attrs[0][1]).group()
                        self.sceneList.append(self.scnID)
                        #print('[ScID:' + self.scnID + ']')

        def handle_endtag(self, tag):
            global CHAPTERS, SCENES
            if tag == 'div':
                if self.docState == S_SCENE:
                    SCENES[self.scnID] = self.sceneText
                    # print(self.sceneText)
                    self.sceneText = ''
                    self.docState = S_CHAPTER
                elif self.docState == S_CHAPTER:
                    CHAPTERS[self.chpID] = self.sceneList
                    # print(self.sceneList)
                    self.sceneList = []
                    self.docState = S_NONE

        def handle_data(self, data):
            if self.docState == S_SCENE:
                if data != ' ':
                    self.sceneText = self.sceneText + data + '\n'

    def convert_html(text):
        """ Convert html into yw7 chapters and scenes. """
        text = format_yw7(text)
        parser = MyHTMLParser()
        parser.feed(text)

    convert_html(text)
    tree = ET.parse(yw7File)
    root = tree.getroot()  # all item attributes


def main():
    """ Call the functions with command line arguments. """
    try:
        htmlPath = sys.argv[1]
    except:
        print('Syntax: htmlyw7.py filename.yw7')
        sys.exit(1)

    prjText = read_file(htmlPath)
    # Read document from html file.

    yw7Path = htmlPath.split('.html')[0] + '.yw7'
    write_yw7(prjText, yw7Path)
    # Convert html to xml and modify .yw7 file.

    for scene in SCENES.values():
        print(scene)
    for chapter in CHAPTERS.values():
        print(chapter)


if __name__ == '__main__':
    main()
