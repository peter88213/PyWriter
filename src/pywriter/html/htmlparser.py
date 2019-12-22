""" PyWriter module

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import re
from html.parser import HTMLParser


class PywHTMLParser(HTMLParser):
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
