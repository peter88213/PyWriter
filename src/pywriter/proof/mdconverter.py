""" PyWriter module

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.proof.mdproject import MdProject
from pywriter.yw7project import Yw7Project


class MdConverter():

    def __init__(self, yw7File, mdFile):
        self.yw7File = yw7File
        self.yw7Prj = Yw7Project(self.yw7File)
        self.mdFile = mdFile
        self.mdPrj = MdProject(self.mdFile)

    def yw7_to_md(self):
        """ Read .yw7 file and convert xml to markdown. """
        if not self.yw7Prj.filePath:
            return('ERROR: "' + self.yw7File + '" is not an yWriter 7 project.')

        if not self.yw7Prj.file_is_present():
            return('ERROR: Project "' + self.yw7File + '" not found.')

        message = self.yw7Prj.read()
        if message.count('ERROR'):
            return(message)

        self.mdPrj.title = self.yw7Prj.title
        self.mdPrj.scenes = self.yw7Prj.scenes
        self.mdPrj.chapters = self.yw7Prj.chapters
        return(self.mdPrj.write())

    def md_to_yw7(self):
        """ Convert markdown to xml and replace .yw7 file. """
        if not self.yw7Prj.filePath:
            return('ERROR: "' + self.yw7File + '" is not an yWriter 7 project.')

        if not self.yw7Prj.file_is_present():
            return('ERROR: Project "' + self.yw7File + '" not found.')
        else:
            self.confirm_overwrite(self.yw7File)

        message = self.yw7Prj.read()
        if message.count('ERROR'):
            return(message)

        if not self.mdPrj.filePath:
            return('ERROR: "' + self.mdFile + '" is not a Markdown file.')

        if not self.mdPrj.file_is_present():
            return('ERROR: "' + self.mdFile + '" not found.')

        message = self.mdPrj.read()
        if message.count('ERROR'):
            return(message)

        prjStructure = self.mdPrj.get_structure()
        if prjStructure == '':
            return('ERROR: Source file contains no yWriter project structure information.')

        if prjStructure != self.yw7Prj.get_structure():
            return('ERROR: Structure mismatch - yWriter project not modified.')

        for scID in self.mdPrj.scenes:
            self.yw7Prj.scenes[scID].sceneContent = self.mdPrj.scenes[scID].sceneContent

        return(self.yw7Prj.write())

    def confirm_overwrite(self, fileName):
        pass
