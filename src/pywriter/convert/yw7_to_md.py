""" PyWriter module

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.mdproject import MdProject
from pywriter.yw7project import Yw7Project


def yw7_to_md(yw7File, mdFile):
    """ Read .yw7 file and convert xml to markdown. """

    YwPrj = Yw7Project(yw7File)
    YwPrj.read()
    MdPrj = MdProject(mdFile)
    MdPrj.title = YwPrj.title
    MdPrj.scenes = YwPrj.scenes
    MdPrj.chapters = YwPrj.chapters
    return(MdPrj.write())


if __name__ == '__main__':
    pass
