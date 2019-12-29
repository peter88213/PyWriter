""" PyWriter module

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.mdproject import MdProject
from pywriter.yw7project import Yw7Project


class MdConverter():

    def confirm_overwrite(self, file):
        pass

    def yw7_to_md(self, yw7File, mdFile):
        """ Read .yw7 file and convert xml to markdown. """

        YwPrj = Yw7Project(yw7File)
        if not YwPrj.filePath:
            return('ERROR: "' + yw7File + '" is not an yWriter 7 project.')

        if not YwPrj.file_is_present():
            return('ERROR: Project "' + yw7File + '" not found.')

        YwPrj.read()
        MdPrj = MdProject(mdFile)
        MdPrj.title = YwPrj.title
        MdPrj.scenes = YwPrj.scenes
        MdPrj.chapters = YwPrj.chapters
        return(MdPrj.write())

    def md_to_yw7(self, mdFile, yw7File):
        """ Convert markdown to xml and replace .yw7 file. """

        YwPrj = Yw7Project(yw7File)
        YwPrj.read()
        if not YwPrj.filePath:
            return('ERROR: "' + yw7File + '" is not an yWriter 7 project.')

        if not YwPrj.file_is_present():
            return('ERROR: Project "' + yw7File + '" not found.')

        else:
            self.confirm_overwrite(yw7File)

        MdPrj = MdProject(mdFile)
        if not MdPrj.filePath:
            return('ERROR: "' + mdFile + '" is not a Markdown file.')

        if not MdPrj.file_is_present():
            return('ERROR: "' + mdFile + '" not found.')

        MdPrj.read()
        prjStructure = MdPrj.getStructure()
        if prjStructure == '':
            return('ERROR: Source file contains no yWriter project structure information.')

        if prjStructure != YwPrj.getStructure():
            return('ERROR: Structure mismatch - yWriter project not modified.')

        for scID in MdPrj.scenes:
            YwPrj.scenes[scID].sceneContent = MdPrj.scenes[scID].sceneContent
        return(YwPrj.write())
