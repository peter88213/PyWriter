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

    # Methods

    add_book
        Attributes
        bkId : string
            the ID of the book to add.
        Add a new book ID to the list. Avoid multiple entries.

    remove_book
        Attributes
        bkId : string
            the ID of the book to remove.
        Remove an existing book ID from the list.       
    """

    def __init__(self, title, desc=''):
        self.title = title
        self.desc = desc
        self.srtBooks = []

    def add_book(self, bkId):
        """Add a new book ID to the list. Avoid multiple entries."""
        if not (bkId in self.srtBooks):
            self.srtBooks.append(bkId)

    def remove_book(self, bkId):
        """Remove an existing book ID from the list."""
        try:
            self.srtBooks.remove(bkId)
        except:
            pass
