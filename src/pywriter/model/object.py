"""Object - represents the basic structure of an object in yWriter.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""


class Object():
    """yWriter object representation.
    # xml: <LOCATIONS><LOCATION> or # xml: <ITEMS><ITEM>
    """

    def __init__(self):
        self.title = None
        # str
        # xml: <Title>

        self.desc = None
        # str
        # xml: <Desc>

        self.tags = None
        # list of str
        # xml: <Tags>

        self.aka = None
        # str
        # xml: <AKA>

    def merge(self, obj):
        """Merge attributes.
        """

        if obj.title:
            # avoids deleting the title, if it is empty by accident
            self.title = obj.title

        if obj.desc is not None:
            self.desc = obj.desc

        if obj.aka is not None:
            self.aka = obj.aka

        if obj.tags is not None:
            self.tags = obj.tags
