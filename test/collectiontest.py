"""Integration tests for the pyWriter project.

Test the collection read and write tasks.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import unittest

from pywriter.model.collection import Collection

from pywriter.model.mdfile import MdFile


TEST_PATH = os.getcwd()
EXEC_PATH = 'yw7/'
DATA_PATH = 'data/collection/'

TEST_FILE = EXEC_PATH + 'collection.pwc'
REFERENCE_FILE = DATA_PATH + 'normal.xml'


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


class NrmOpr(unittest.TestCase):
    """Test case: Normal operation

        Condition: yw7 file is present and read/writeable. 
        Expected result: During the whole process, the markdown 
            file's content matches the reference. 
    """

    def setUp(self):
        remove_all_testfiles()
        copy_file(REFERENCE_FILE,
                  TEST_FILE)

    def test_config_rw(self):
        """Read and write the configuration file. """

        myCollection = Collection(TEST_FILE)
        myCollection.read()

        os.remove(TEST_FILE)

        myCollection.write()

        self.assertEqual(read_file(TEST_FILE),
                         read_file(REFERENCE_FILE))


def main():
    unittest.main()


if __name__ == '__main__':
    main()
