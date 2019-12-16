""" Import proofed chapters. 

Read a html file divided into ChID:x and ScID:y sections 
and replace the scenes in an yw7 project file.

For further information see https://github.com/peter88213/yWrestler
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys
import re
from html.parser import HTMLParser
import ywrestler

PROGRAM_TITLE = 'Import yw7 scenes from html'


def format_yw7(text):
    """ Convert html markup to yw7 raw markup """
    text = re.sub('<i.*?>|<I.*?>|<em.*?>|<EM.*?>', '[i]', text)
    text = re.sub('</i>|</I>|</em>|</EM>', '[/i]', text)
    text = re.sub('<b.*?>|<B.*?>|<strong.*?>|<STRONG.*?>', '[b]', text)
    text = re.sub('</b>|</B>|</strong><|</STRONG>', '[/b]', text)
    text = text.replace('\n', '')
    text = text.replace('\t', ' ')
    while text.count('  '):
        text = text.replace('  ', ' ')
    return(text)


def count_words(text):
    """ Required, because yWriter stores word counts. """
    text = re.sub('\[.+?\]|\.|\,| -', '', text)
    # Remove yw7 raw markup
    wordList = text.split()
    wordCount = len(wordList)
    return str(wordCount)


def count_letters(text):
    """ Required, because yWriter stores letter counts. """
    text = re.sub('\[.+?\]', '', text)
    # Remove yw7 raw markup
    letterCount = len(text)
    return str(letterCount)


class MyHTMLParser(HTMLParser):
    """ Collect scene contents in a dictionary. """
    sceneText = ''
    scID = 0
    inScene = False
    sceneContents = {}

    def get_scene_contents(self):
        """ Export scene content dictionary. """
        return(self.sceneContents)

    def handle_starttag(self, tag, attrs):
        """ Get scene ID at scene start. """
        if tag == 'div':
            if attrs[0][0] == 'id':
                if attrs[0][1].count('ScID'):
                    self.inScene = True
                    self.scID = re.search('[0-9]+', attrs[0][1]).group()

    def handle_endtag(self, tag):
        """ Save scene content in dictionary at scene end. """
        if tag == 'div':
            if self.inScene:
                self.sceneContents[self.scID] = self.sceneText
                self.sceneText = ''
                self.inScene = False

    def handle_data(self, data):
        """ Collect paragraphs within scene. """
        if self.inScene:
            if data != ' ':
                self.sceneText = self.sceneText + data + '\n'


def html_to_yw7(htmlFile, yw7File):
    """ Convert html into yw7 sceneContents and modify .yw7 file. """
    try:
        with open(htmlFile, 'r', encoding='utf-8') as f:
            text = (f.read())
    except:
        try:
            with open(htmlFile, 'r') as f:
                text = (f.read())
        except(FileNotFoundError):
            return('\nERROR: "' + htmlFile + '" not found.')

    text = format_yw7(text)

    parser = MyHTMLParser()
    parser.feed(text)
    prj = ywrestler.Project(yw7File)

    return(prj.write_scene_contents(parser.get_scene_contents()))


def main():
    print('\n*** ' + PROGRAM_TITLE + ' ***')
    try:
        htmlPath = sys.argv[1]
    except(IndexError):
        htmlPath = input('\nEnter html filename: ')

    yw7Path = htmlPath.split('.html')[0] + '.yw7'

    print('\nWARNING: This will overwrite "' +
          yw7Path + '" (if exists)!')
    userConfirmation = input('Continue (y/n)? ')
    if userConfirmation in ('y', 'Y'):
        print(html_to_yw7(htmlPath, yw7Path))
    else:
        print('Program abort by user.\n')
    input('Press ENTER to continue ...')


if __name__ == '__main__':
    main()
