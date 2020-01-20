"""Integration tests for the pyWriter project.

Test the Use Cases "manage the collection".

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import unittest

from pywriter.model.collection import Collection

from pywriter.model.bookdesc import BookDesc

from pywriter.model.mdfile import MdFile
from distutils.tests.test_text_file import TEST_DATA


TEST_PATH = os.getcwd()
EXEC_PATH = 'yw7/'
DATA_PATH = 'data/collection/'

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


class NrmOpr(unittest.TestCase):
    """Test case: Normal operation
    """

    def setUp(self):
        remove_all_testfiles()

        try:
            os.mkdir('yw7/yWriter Projects')
        except:
            pass
        try:
            os.mkdir('yw7\yWriter Projects/The Gravity Monster.yw')
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

    def test_read_write_configuration(self):
        """Read and write the configuration file. """
        copy_file('data/collection/read_write.xml', TEST_FILE)
        myCollection = Collection(TEST_FILE)
        myCollection.read()
        os.remove(TEST_FILE)
        myCollection.write()
        self.assertEqual(read_file(TEST_FILE),
                         read_file('data/collection/read_write.xml'))

    def test_create_collection(self):
        """Use Case: manage the collection/create the collection."""
        myCollection = Collection(TEST_FILE)
        myCollection.write()
        self.assertEqual(read_file(TEST_FILE),
                         read_file('data/collection/create_collection.xml'))

    def test_add_book(self):
        """Use Case: manage the collection/add a book to the collection."""
        copy_file(DATA_PATH + 'create_collection.xml', TEST_FILE)
        myCollection = Collection(TEST_FILE)
        myCollection.read()

        myCollection.add_book(
            'yw7\yWriter Projects/The Gravity Monster.yw/The Gravity Monster.yw7')
        myCollection.write()
        self.assertEqual(read_file(TEST_FILE),
                         read_file('data/collection/add_first_book.xml'))

        myCollection.add_book(
            'yw7\yWriter Projects/The Refugee Ship.yw/The Refugee Ship.yw7')
        myCollection.write()
        self.assertEqual(read_file(TEST_FILE),
                         read_file('data/collection/add_second_book.xml'))

    def test_remove_book(self):
        """Use Case: manage the collection/remove a book from the collection."""
        copy_file(DATA_PATH + 'add_second_book.xml', TEST_FILE)
        myCollection = Collection(TEST_FILE)
        myCollection.read()

        myCollection.remove_book('1')
        myCollection.write()
        self.assertEqual(read_file(TEST_FILE),
                         read_file('data/collection/remove_book.xml'))

        myCollection.remove_book('2')
        myCollection.write()
        self.assertEqual(read_file(TEST_FILE),
                         read_file('data/collection/create_collection.xml'))

    def test_create_series(self):
        """Use Case: manage book series/create a series."""
        copy_file(DATA_PATH + 'add_first_book.xml', TEST_FILE)
        myCollection = Collection(TEST_FILE)
        myCollection.read()

        myCollection.add_series('Rick Starlift')
        myCollection.write()
        self.assertEqual(read_file(TEST_FILE),
                         read_file('data/collection/empty_series.xml'))

    def test_remove_series(self):
        """Use Case: manage book series/remove a series."""
        copy_file(DATA_PATH + 'empty_series.xml', TEST_FILE)
        myCollection = Collection(TEST_FILE)
        myCollection.read()

        myCollection.remove_series('Rick Starlift')
        myCollection.write()
        self.assertEqual(read_file(TEST_FILE),
                         read_file('data/collection/add_first_book.xml'))

    def test_add_book_to_series(self):
        """Use Case: manage book series/add a book to a series."""
        copy_file(DATA_PATH + 'empty_series.xml', TEST_FILE)
        myCollection = Collection(TEST_FILE)
        myCollection.read()
        for series in myCollection.srtSeries:
            if series.title == 'Rick Starlift':
                series.add_book('1')
                break

        myCollection.write()
        self.assertEqual(read_file(TEST_FILE),
                         read_file('data/collection/add_book_to_series.xml'))

    def test_remove_book_from_series(self):
        """Use Case: manage book series/remove a book from a series."""
        copy_file(DATA_PATH + 'add_book_to_series.xml', TEST_FILE)
        myCollection = Collection(TEST_FILE)
        myCollection.read()
        for series in myCollection.srtSeries:
            if series.title == 'Rick Starlift':
                series.remove_book('1')
                break

        myCollection.write()
        self.assertEqual(read_file(TEST_FILE),
                         read_file('data/collection/empty_series.xml'))

    def test_write_descriptions(self):
        """Use Case: edit a series description and book descriptions."""
        copy_file(DATA_PATH + 'two_in_series.xml', TEST_FILE)
        myCollection = Collection(TEST_FILE)
        myCollection.read()

        myBookdesc = BookDesc(EXEC_PATH + 'Rick Starlift_series.html')
        for series in myCollection.srtSeries:
            if series.title == 'Rick Starlift':
                myBookdesc.write(series, myCollection)

        self.assertEqual(read_file(EXEC_PATH + 'Rick Starlift_series.html'),
                         read_file('data/collection/two_in_series.html'))

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
                         read_file('data/collection/add_descriptions.xml'))


def main():
    unittest.main()


if __name__ == '__main__':
    main()
