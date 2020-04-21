"""PyWriter Office development

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import sys
import os

from pywriter.collection.collection import Collection
from pywriter.collection.pywoffice import PywOffice

DEFAULT_CONF_PATH = '.pywriter'
DEFAULT_FILE = 'collection.pwc'


def run(configPath):
    myCollection = Collection(configPath)
    myCollection.read()

    for ser in myCollection.srtSeries:
        print(ser.title)
        for bkId in ser.srtBooks:
            print('    ' + myCollection.books[bkId].title +
                  ': ' + myCollection.books[bkId].filePath)

    print('')
    for bkId in myCollection.books:
        print(myCollection.books[bkId].title +
              ': ' + myCollection.books[bkId].filePath)

    myOffice = PywOffice(myCollection)


if __name__ == '__main__':
    try:
        configPath = sys.argv[1]
    except:
        configPath = ''

    if not os.path.isfile(configPath):
        home = os.path.expanduser("~")
        try:
            pywPath = home + '/' + DEFAULT_CONF_PATH
            os.mkdir(pywPath)
        except:
            pass

        configPath = pywPath + '/' + DEFAULT_FILE

    run(configPath)
