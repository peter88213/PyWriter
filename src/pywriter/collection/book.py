"""Book - represents the basic structure of a book in yWriter.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os

from pywriter.model.yw7file import Yw7File


class Book():
    """yWriter scene representation.

    # Attributes

    title : str
        the book title.

    desc : str
        the book summary.

    filePath : str
        location of the book project folder.

    wordCount : int 
        the book's scenes total word count.

    letterCount : int 
        the book's scenes total letter count.

    # Methods

    update
        Open the yw7 file, read title and description, 
        and compute word count and letter count. 
    """

    def __init__(self, filePath: str) -> None:
        self.title = ''
        self.desc = ''
        self.wordCount = 0
        self.letterCount = 0
        self.filePath = filePath
        self.retrieve_book_data()

    def retrieve_book_data(self) -> None:
        book = Yw7File(self.filePath)
        book.read()
        self.title = book.title
        self.desc = book.desc

        self.wordCount = 0
        self.letterCount = 0

        for scId in book.scenes:
            self.wordCount = self.wordCount + book.scenes[scId].wordCount
            self.letterCount = self.letterCount + book.scenes[scId].letterCount

        del book

    def put_book_data(self) -> None:
        book = Yw7File(self.filePath)
        book.read()
        modified = False

        if self.title != book.title:
            book.title = self.title
            modified = True

        if self.desc != book.desc:
            book.desc = self.desc
            modified = True

        if modified:
            book.write(book)

        del book
