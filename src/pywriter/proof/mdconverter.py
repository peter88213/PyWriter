"""PyWriter module

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.proof.mdfile import MdFile
from pywriter.core.yw7file import Yw7File


class MdConverter():

    def __init__(self, yw7Path, mdPath):
        self.yw7Path = yw7Path
        self.yw7File = Yw7File(self.yw7Path)
        self.mdPath = mdPath
        self.mdFile = MdFile(self.mdPath)

    def yw7_to_md(self):
        """Read .yw7 file and convert xml to markdown. """

        if self.yw7File.filePath is None:
            return('ERROR: "' + self.yw7Path + '" is not an yWriter 7 project.')

        if not self.yw7File.file_exists():
            return('ERROR: Project "' + self.yw7Path + '" not found.')

        message = self.yw7File.read()
        if message.startswith('ERROR'):
            return(message)

        self.mdFile.title = self.yw7File.title
        self.mdFile.scenes = self.yw7File.scenes
        self.mdFile.chapters = self.yw7File.chapters
        return(self.mdFile.write())

    def md_to_yw7(self):
        """Convert markdown to xml and replace .yw7 file. """

        if self.yw7File.filePath is None:
            return('ERROR: "' + self.yw7Path + '" is not an yWriter 7 project.')

        if not self.yw7File.file_exists():
            return('ERROR: Project "' + self.yw7Path + '" not found.')
        else:
            if not self.confirm_overwrite(self.yw7Path):
                return('Program abort by user.')

        message = self.yw7File.read()
        if message.startswith('ERROR'):
            return(message)

        if self.mdFile.filePath is None:
            return('ERROR: "' + self.mdPath + '" is not a Markdown file.')

        if not self.mdFile.file_exists():
            return('ERROR: "' + self.mdPath + '" not found.')

        message = self.mdFile.read()
        if message.startswith('ERROR'):
            return(message)

        prjStructure = self.mdFile.get_structure()
        if prjStructure == '':
            return('ERROR: Source file contains no yWriter project structure information.')

        if prjStructure != self.yw7File.get_structure():
            return('ERROR: Structure mismatch - yWriter project not modified.')

        for scID in self.mdFile.scenes:
            self.yw7File.scenes[scID].sceneContent = self.mdFile.scenes[scID].sceneContent

        return(self.yw7File.write())

    def confirm_overwrite(self, fileName):
        return(True)
