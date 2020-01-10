"""Import and export yWriter 7 data. 

yWriter 7 standalone file converter with basic error handling 

The tests below may be included in the 'XyFile' classes at a later date.

Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""


class Yw7Cnv():

    def yw7_to_document(self, yw7File, documentFile):
        """Read .yw7 file and convert xml to a document file. """

        if yw7File.is_locked():
            return('ERROR: yWriter 7 seems to be open. Please close first.')

        if yw7File.filePath is None:
            return('ERROR: "' + yw7File.filePath + '" is not an yWriter 7 project.')

        message = yw7File.read()

        if message.startswith('ERROR'):
            return(message)

        if documentFile.file_exists():

            if not self.confirm_overwrite(documentFile.filePath):
                return('Program abort by user.')

        return(documentFile.write(yw7File))

    def document_to_yw7(self, documentFile, yw7File):
        """Read document file, convert its content to xml, and replace .yw7 file. """

        if yw7File.is_locked():
            return('ERROR: yWriter 7 seems to be open. Please close first.')

        if yw7File.filePath is None:
            return('ERROR: "' + yw7File.filePath + '" is not an yWriter 7 project.')

        if not yw7File.file_exists():
            return('ERROR: Project "' + yw7File.filePath + '" not found.')

        else:

            if not self.confirm_overwrite(yw7File.filePath):
                return('Program abort by user.')

        if documentFile.filePath is None:
            return('ERROR: "' + documentFile.filePath + '" is not of the supported type.')

        if not documentFile.file_exists():
            return('ERROR: "' + documentFile.filePath + '" not found.')

        message = documentFile.read()

        if message.startswith('ERROR'):
            return(message)

        prjStructure = documentFile.get_structure()

        if prjStructure == '':
            return('ERROR: Source file contains no yWriter project structure information.')

        message = yw7File.read()
        # initialize yw7File data

        if message.startswith('ERROR'):
            return(message)

        ''' The structure test shown below does not work for ChapterDesc import
       if prjStructure != yw7File.get_structure():
            return('ERROR: Structure mismatch - yWriter project not modified.')
        '''

        return(yw7File.write(documentFile))

    def confirm_overwrite(self, fileName):
        return(True)
