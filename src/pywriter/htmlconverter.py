""" PyWriter module

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.htmlproject import HTMLProject
from pywriter.yw7project import Yw7Project


class HtmlConverter():

    def confirm_overwrite(self, file):
        return(True)

    def html_to_yw7(self, htmlFile, yw7File):
        """ Convert html into yw7 newContents and modify .yw7 file. """

        YwPrj = Yw7Project(yw7File)
        YwPrj.read()
        if not YwPrj.filePath:
            return('ERROR: "' + yw7File + '" is not an yWriter 7 project.')

        if not YwPrj.file_is_present():
            return('ERROR: Project "' + yw7File + '" not found.')

        else:
            self.confirm_overwrite(yw7File)

        HtmlPrj = HTMLProject(htmlFile)
        if not HtmlPrj.filePath:
            return('ERROR: "' + htmlFile + '" is not a HTML file.')

        if not HtmlPrj.file_is_present():
            return('ERROR: "' + htmlFile + '" not found.')

        HtmlPrj.read()
        prjStructure = HtmlPrj.getStructure()
        if prjStructure == '':
            return('ERROR: Source file contains no yWriter project structure information.')

        if prjStructure != YwPrj.getStructure():
            return('ERROR: Structure mismatch - yWriter project not modified.')

        for scID in HtmlPrj.scenes:
            YwPrj.scenes[scID].sceneContent = HtmlPrj.scenes[scID].sceneContent
        return(YwPrj.write())

    def yw7_to_html(self, yw7File, htmlFile):
        """ Read .yw7 file and convert sceneContents to html. """

        YwPrj = Yw7Project(yw7File)
        if not YwPrj.filePath:
            return('ERROR: "' + yw7File + '" is not an yWriter 7 project.')

        if not YwPrj.file_is_present():
            return('ERROR: Project "' + yw7File + '" not found.')

        YwPrj.read()
        HtmlPrj = HTMLProject(htmlFile)
        if HtmlPrj.file_is_present():
            self.confirm_overwrite(htmlFile)

        HtmlPrj.title = YwPrj.title
        HtmlPrj.scenes = YwPrj.scenes
        HtmlPrj.chapters = YwPrj.chapters
        return(HtmlPrj.write())
