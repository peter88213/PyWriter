""" PyWriter module

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from pywriter.model.novel import Novel


def yw7_to_csv(yw7Path, csvPath):
    """ Create scenes link list """

    prj = Novel()
    prj.read(yw7Path)
    with open(csvPath, 'w') as f:
        for chID in prj.chapters:
            for scID in prj.chapters[chID].scenes:
                f.write(scID + ',"')
                for line in prj.scenes[scID].desc:
                    f.write(line.replace('"', "'"))
                f.write('"\n')


if __name__ == '__main__':
    pass
