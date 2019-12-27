""" PyWriter module

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.htmlproject import HTMLProject
from pywriter.yw7project import Yw7Project


def html_to_yw7(htmlFile, yw7File):
    """ Convert html into yw7 newContents and modify .yw7 file. """

    YwPrj = Yw7Project(yw7File)
    YwPrj.read()
    HTMLPrj = HTMLProject(htmlFile)
    HTMLPrj.read()
    htmlStruct = HTMLPrj.getStructure()
    yw7Struct = YwPrj.getStructure()
    if htmlStruct == yw7Struct:
        for scID in HTMLPrj.scenes:
            YwPrj.scenes[scID].sceneContent = HTMLPrj.scenes[scID].sceneContent
        return(YwPrj.write())
    else:
        return('\nERROR: Structure mismatch - yWriter project not modified.')


if __name__ == '__main__':
    pass
