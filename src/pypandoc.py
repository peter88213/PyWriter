"""" A simple Pandoc wrapper for the PyWriter project

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os


def convert_file(srcFile, dstFormat, format='', outputfile='', extra_args=[]):
    """ Let pandoc read .docx file and convert to markdown. """

    temporaryFile = 'temp.txt'

    extraArgs = ' '
    for extraArgument in extra_args:
        extraArgs = extraArgs + extraArgument + ' '

    if outputfile != '':
        dstFile = ' -o ' + outputfile
    else:
        dstFile = ' -o ' + temporaryFile

    os.system('pandoc.exe -w ' + dstFormat + ' -r ' +
              format + dstFile + ' ' + extraArgs + srcFile)

    if outputfile == '':
        with open(temporaryFile, 'r', encoding='utf-8') as f:
            result = f.read()
        os.remove(temporaryFile)
        return(result)


if __name__ == '__main__':
    pass
