""" PyWriter module

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.edit.htmlfile import HtmlFile
from pywriter.core.yw7file import Yw7File


class ContentConverter():

    def __init__(self, yw7Path, htmlFile):
        self.yw7Path = yw7Path
        self.yw7File = Yw7File(self.yw7Path)
        self.htmlFile = htmlFile
        self.htmlPrj = HtmlFile(self.htmlFile)

    def yw7_to_html(self):
        """ Read .yw7 file and convert sceneContents to html. """
        if not self.yw7File.filePath:
            return('ERROR: "' + self.yw7Path + '" is not an yWriter 7 project.')

        if not self.yw7File.file_is_present():
            return('ERROR: Project "' + self.yw7Path + '" not found.')

        message = self.yw7File.read()
        if message.count('ERROR'):
            return(message)

        if self.htmlPrj.file_is_present():
            self.confirm_overwrite(self.htmlFile)

        self.htmlPrj.title = self.yw7File.title
        self.htmlPrj.scenes = self.yw7File.scenes
        self.htmlPrj.chapters = self.yw7File.chapters
        return(self.htmlPrj.write())

    def html_to_yw7(self):
        """ Convert html into yw7 newContents and modify .yw7 file. """
        if not self.yw7File.filePath:
            return('ERROR: "' + self.yw7Path + '" is not an yWriter 7 project.')

        if not self.yw7File.file_is_present():
            return('ERROR: Project "' + self.yw7Path + '" not found.')
        else:
            self.confirm_overwrite(self.yw7Path)

        message = self.yw7File.read()
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

        if prjStructure != self.yw7File.get_structure():
            return('ERROR: Structure mismatch - yWriter project not modified.')

        for scID in self.htmlPrj.scenes:
            self.yw7File.scenes[scID].sceneContent = self.htmlPrj.scenes[scID].sceneContent

        return(self.yw7File.write())

    def confirm_overwrite(self, fileName):
        pass
