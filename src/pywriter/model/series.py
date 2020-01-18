"""Series - represents the basic structure of a book series in yWriter.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""


class Series():
    """yWriter series representation.

    # Attributes

    title : str
        the series title.

    desc : str
        the series description.

    srtBooks : list 
        the series' book IDs. The order of its elements 
        corresponds to the series' order of the books.
    """

    def __init__(self):
        self.title = ''
        self.desc = ''
        self.srtBooks = []
