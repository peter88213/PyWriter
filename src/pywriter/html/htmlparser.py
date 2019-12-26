""" PyWriter module

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import re
from html.parser import HTMLParser
from pywriter.project import PywProject


class PywHTMLParser(HTMLParser):
    """ Collect scene contents in a dictionary. """

    sceneText = ''
    scID = 0
    chID = 0
    inScene = False
    prj = PywProject()

    def get_prj(self):
        """ Export scene content dictionary. """
        return(self.prj)

    def handle_starttag(self, tag, attrs):
        """ Get scene ID at scene start. """
        if tag == 'div':
            if attrs[0][0] == 'id':
                if attrs[0][1].count('ScID'):
                    self.scID = re.search('[0-9]+', attrs[0][1]).group()
                    self.prj.scenes[self.scID] = PywProject.Scene()
                    self.prj.chapters[self.chID].scenes.append(self.scID)
                    self.inScene = True
                elif attrs[0][1].count('ChID'):
                    self.ChID = re.search('[0-9]+', attrs[0][1]).group()
                    self.prj.chapters[self.chID] = PywProject.Chapter()

    def handle_endtag(self, tag):
        """ Save scene content in dictionary at scene end. """
        if tag == 'div':
            if self.inScene:
                self.prj.scenes[self.scID].sceneContent = self.sceneText
                self.sceneText = ''
                self.inScene = False

    def handle_data(self, data):
        """ Collect paragraphs within scene. """
        if self.inScene:
            if data != ' ':
                self.sceneText = self.sceneText + data + '\n'
