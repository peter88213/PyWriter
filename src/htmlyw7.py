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
    """ Collect scene contents in a dictionary. """
    sceneText = ''
    scnID = 0
    inScene = False
    scenes = {}

    def getScenes(self):
        """ Export scene content dictionary. """
        return(self.scenes)

    def handle_starttag(self, tag, attrs):
        """ Get scene ID at scene start. """
        if tag == 'div':
            if attrs[0][0] == 'id':
                if attrs[0][1].count('ScID'):
                    self.inScene = True
                    self.scnID = re.search('[0-9]+', attrs[0][1]).group()

    def handle_endtag(self, tag):
        """ Save scene content in dictionary at scene end. """
        if tag == 'div':
            if self.inScene:
                self.scenes[self.scnID] = self.sceneText
                self.sceneText = ''
                self.inScene = False

    def handle_data(self, data):
        """ Collect paragraphs within scene. """
        if self.inScene:
            if data != ' ':
                self.sceneText = self.sceneText + data + '\n'


def html_to_yw7(htmlFile, yw7File):
    """ Convert html into yw7 scenes and modify .yw7 file. """
    try:
        with open(htmlFile, 'r') as f:
            text = (f.read())
    except(IOError):
        sys.exit(1)

    text = format_yw7(text)

    parser = MyHTMLParser()
    parser.feed(text)
    scenes = parser.getScenes()

    tree = ET.parse(yw7File)
    root = tree.getroot()

    for scn in root.iter('SCENE'):
        scnID = scn.find('ID').text
        scn.find('SceneContent').text = scenes[scnID]
    tree.write(yw7File)


def main():
    """ Call the functions with command line arguments. """
    try:
        htmlPath = sys.argv[1]
    except:
        print('Syntax: htmlyw7.py filename.html')
        sys.exit(1)

    yw7Path = htmlPath.split('.html')[0] + '.yw7'
    html_to_yw7(htmlPath, yw7Path)


if __name__ == '__main__':
    main()
