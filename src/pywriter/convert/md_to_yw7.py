""" PyWriter module

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.mdproject import MdProject
from pywriter.yw7project import Yw7Project


def md_to_yw7(mdFile, yw7File):
    """ Convert markdown to xml and replace .yw7 file. """

    YwPrj = Yw7Project(yw7File)
    YwPrj.read()
    MdPrj = MdProject(mdFile)
    MdPrj.read()
    for scID in MdPrj.scenes:
        YwPrj.scenes[scID].sceneContent = MdPrj.scenes[scID].sceneContent
    return(YwPrj.write())


if __name__ == '__main__':
    pass
