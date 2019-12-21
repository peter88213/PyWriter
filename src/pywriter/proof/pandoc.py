'''
Created on 21.12.2019

@author: Peter
'''
import os


def convert_file(srcFile, dstFormat, format='', outputfile='', extra_args=[]):
    """ Pandoc wrapper emulating the pypandoc.convert_file functon. """

    temporaryFile = 'temp.txt'

    extraArgs = ' '
    for extraArgument in extra_args:
        extraArgs = extraArgs + extraArgument + ' '

    if outputfile != '':
        dstFile = outputfile
    else:
        dstFile = temporaryFile

    argument1 = 'pandoc.exe'
    argument2 = ' -w ' + dstFormat
    argument3 = ' -r ' + format
    argument4 = ' -o "' + dstFile + '"'
    argument5 = ' ' + extraArgs
    argument6 = ' "' + srcFile + '"'

    status = os.system(argument1 + argument2 + argument3 +
                       argument4 + argument5 + argument6)

    if status == 0:
        if outputfile == '':
            with open(temporaryFile, 'r', encoding='utf-8') as f:
                result = f.read()
            os.remove(temporaryFile)
            return(result)


if __name__ == '__main__':
    pass
