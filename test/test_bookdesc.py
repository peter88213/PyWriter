"""Integration tests for the pyWriter project.

Test the Use Cases "manage the collection".

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import unittest

from pywriter.collection.collection import Collection

from pywriter.collection.bookdesc import BookDesc


TEST_PATH = os.getcwd()
EXEC_PATH = 'yw7/'
DATA_PATH = 'data/_collection/'

TEST_FILE = EXEC_PATH + 'collection.pwc'


def read_file(inputFile):
    with open(inputFile, 'r', encoding='utf-8') as f:
        return(f.read())


def copy_file(inputFile, outputFile):
    with open(inputFile, 'rb') as f:
        myData = f.read()
    with open(outputFile, 'wb') as f:
        f.write(myData)
    return()


def remove_all_testfiles():
    try:
        os.remove(TEST_FILE)
    except:
        pass


class devel(unittest.TestCase):

    def setUp(self):
        remove_all_testfiles()

        try:
            os.mkdir('yw7/yWriter Projects')
        except:
            pass
        try:
            os.mkdir('yw7/yWriter Projects/The Gravity Monster.yw')
        except:
            pass
        copy_file('data/yWriter Projects/The Gravity Monster.yw/The Gravity Monster.yw7',
                  'yw7/yWriter Projects/The Gravity Monster.yw/The Gravity Monster.yw7')
        try:
            os.mkdir('yw7\yWriter Projects/The Refugee Ship.yw')
        except:
            pass
        copy_file('data/yWriter Projects/The Refugee Ship.yw/The Refugee Ship.yw7',
                  'yw7/yWriter Projects/The Refugee Ship.yw/The Refugee Ship.yw7')

    def test_read_descriptions(self):
        """Use Case: edit a series description and book descriptions."""
        copy_file(DATA_PATH + 'two_in_series.xml', TEST_FILE)
        copy_file(DATA_PATH + 'add_descriptions.html',
                  EXEC_PATH + 'Rick Starlift_series.html')
        myCollection = Collection(TEST_FILE)
        myCollection.read()

        myBookdesc = BookDesc(EXEC_PATH + 'Rick Starlift_series.html')
        for series in myCollection.srtSeries:
            if series.title == 'Rick Starlift':
                myBookdesc.read(series, myCollection)

        myCollection.write()
        self.assertEqual(read_file(TEST_FILE),
                         read_file(DATA_PATH + '/add_descriptions.xml'))


def main():
    unittest.main()


if __name__ == '__main__':
    main()
