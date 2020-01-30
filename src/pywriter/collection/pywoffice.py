"""yWriter project manager

Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from tkinter import *

TITLE = 'PyWriter Office v2.0.0'


class PywOffice():
    """
    classdocs
    """

    def showDesc(self, event):
        choice = self.listbox.curselection()[0]
        self.processInfo.config(
            text=self.collection.books[self.booklist[choice]].desc)

    def __init__(self, collection):
        """
        Constructor
        """
        self.collection = collection

        root = Tk()
        root.geometry("800x300")
        root.title(TITLE)
        self.header = Label(root, text=__doc__)
        self.header.pack(padx=5, pady=5)
        self.appInfo = Label(root, text='')
        self.appInfo.pack(padx=5, pady=5)
        self.processInfo = Label(root, text='')
        self.processInfo.pack(padx=5, pady=5)

        self.listbox = Listbox(root, selectmode=SINGLE)
        self.booklist = []
        for bkId in collection.books:
            self.booklist.append(bkId)
            self.listbox.insert(END, collection.books[bkId].title)
        self.listbox.pack()
        self.listbox.bind('<Button-1>', self.showDesc)

        root.quitButton = Button(text="OK", command=quit)
        root.quitButton.config(height=1, width=10)
        root.quitButton.pack(padx=5, pady=5)
        root.mainloop()
