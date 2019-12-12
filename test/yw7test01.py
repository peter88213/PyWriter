""" Python unit tests for the yWrestler project.

For further information see https://github.com/peter88213/yWrestler
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import unittest
import yw7
import yw7read

YW7_FILE = 'yWriter7 Sample/yW7 Sample Project.yw7'


class NormalOperation(unittest.TestCase):
    """ Test case: Normal operation

        Condition: xml import is successful. 
        Expected result: converted string matches the refData string. 
    """

    def test_read(self):
        self.assertEqual(yw7read.read_xml(YW7_FILE), yw7.refData)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
