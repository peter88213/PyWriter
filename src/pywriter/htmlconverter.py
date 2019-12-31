""" PyWriter module

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.htmlproject import HtmlProject
from pywriter.yw7project import Yw7Project


class HtmlConverter():

    def __init__(self, yw7File, htmlFile):
        self.yw7File = yw7File
        self.yw7Prj = Yw7Project(self.yw7File)
        self.htmlFile = htmlFile
        self.htmlPrj = HtmlProject(self.htmlFile)

    def yw7_to_html(self):
        """ Read .yw7 file and convert sceneContents to html. """
        if not self.yw7Prj.filePath:
            return('ERROR: "' + self.yw7File + '" is not an yWriter 7 project.')

        if not self.yw7Prj.file_is_present():
            return('ERROR: Project "' + self.yw7File + '" not found.')

        message = self.yw7Prj.read()
        if message.count('ERROR'):
            return(message)

        if self.htmlPrj.file_is_present():
            self.confirm_overwrite(self.htmlFile)

        self.htmlPrj.title = self.yw7Prj.title
        self.htmlPrj.scenes = self.yw7Prj.scenes
        self.htmlPrj.chapters = self.yw7Prj.chapters
        return(self.htmlPrj.write())

    def html_to_yw7(self):
        """ Convert html into yw7 newContents and modify .yw7 file. """
        if not self.yw7Prj.filePath:
            return('ERROR: "' + self.yw7File + '" is not an yWriter 7 project.')

        if not self.yw7Prj.file_is_present():
            return('ERROR: Project "' + self.yw7File + '" not found.')
        else:
            self.confirm_overwrite(self.yw7File)

        message = self.yw7Prj.read()
        if message.count('ERROR'):
            return(message)

        if not self.htmlPrj.filePath:
            return('ERROR: "' + self.htmlFile + '" is not a HTML file.')

        if not self.htmlPrj.file_is_present():
            return('ERROR: "' + self.htmlFile + '" not found.')

        message = self.htmlPrj.read()
        if message.count('ERROR'):
            return(message)

        prjStructure = self.htmlPrj.get_structure()
        if prjStructure == '':
            return('ERROR: Source file contains no yWriter project structure information.')

        if prjStructure != self.yw7Prj.get_structure():
            return('ERROR: Structure mismatch - yWriter project not modified.')

        for scID in self.htmlPrj.scenes:
            self.yw7Prj.scenes[scID].sceneContent = self.htmlPrj.scenes[scID].sceneContent

        return(self.yw7Prj.write())

    def confirm_overwrite(self, fileName):
        pass
