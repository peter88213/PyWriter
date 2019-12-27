""" PyWriter module

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.htmlproject import HTMLProject
from pywriter.yw7project import Yw7Project


def yw7_to_html(yw7File, htmlFile):
    """ Read .yw7 file and convert sceneContents to html. """

    YwPrj = Yw7Project(yw7File)
    YwPrj.read()
    HTMLPrj = HTMLProject(htmlFile)
    HTMLPrj.title = YwPrj.title
    HTMLPrj.scenes = YwPrj.scenes
    HTMLPrj.chapters = YwPrj.chapters
    return(HTMLPrj.write())


if __name__ == '__main__':
    pass
