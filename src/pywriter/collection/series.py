"""Series - represents the basic structure of a book series in yWriter.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""


class Series():
    """yWriter book series representation.    
    """

    def __init__(self, title: str, desc: str = '') -> None:
        self.title = title
        self.summary = desc
        self.srtBooks = []

    def add_book(self, bkId: str) -> None:
        """Add a new book ID to the list. Avoid multiple entries.
        """
        if not (bkId in self.srtBooks):
            self.srtBooks.append(bkId)

    def remove_book(self, bkId: str) -> str:
        """Remove an existing book ID from the list.       
        Return a message beginning with SUCCESS or ERROR.
        """
        try:
            self.srtBooks.remove(bkId)
            return 'SUCCESS'

        except:
            return 'ERROR'
