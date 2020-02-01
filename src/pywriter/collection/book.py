"""Book - represents the basic structure of a book in yWriter.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os

from pywriter.model.yw7file import Yw7File


class Book():
    """yWriter book representation."""

    def __init__(self, filePath: str) -> None:
        self.title = ''
        self.summary = ''
        self.wordCount = 0
        self.letterCount = 0
        self.filePath = filePath
        self.retrieve_book_data()

    def retrieve_book_data(self) -> None:
        """Open the yw7 file, read title and summary, 
        and compute word count and letter count.
        """
        book = Yw7File(self.filePath)
        book.read()
        self.title = book.title
        self.summary = book.summary

        self.wordCount = 0
        self.letterCount = 0

        for scId in book.scenes:
            self.wordCount = self.wordCount + book.scenes[scId].wordCount
            self.letterCount = self.letterCount + book.scenes[scId].letterCount

        del book

    def put_book_data(self) -> None:
        """Open the yw7 file, write title and summary."""
        book = Yw7File(self.filePath)
        book.read()
        modified = False

        if self.title != book.title:
            book.title = self.title
            modified = True

        if self.summary != book.summary:
            book.summary = self.summary
            modified = True

        if modified:
            book.write(book)

        del book
