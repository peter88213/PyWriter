""" Build python scripts for the PyWriter distributions.
        
In order to distribute single scripts without dependencies, 
this script "inlines" all modules imported from the pywriter package.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import re
import os

SRC = '../src/'
BUILD = '../test/'
PACKAGE = 'pywriter'


def inline_module(file, text, processedModules):
    with open(file, 'r') as f:
        print('Processing "' + file + '"...')
        lines = f.readlines()
        inSuppressedComment = False
        for line in lines:
            if line.count('"""') == 1:
                if file.count(PACKAGE):
                    if inSuppressedComment:
                        inSuppressedComment = False
                    else:
                        inSuppressedComment = True
                else:
                    text = text + line
            elif not inSuppressedComment:
                if file.count(PACKAGE):
                    if line.count('main()'):
                        return(text)

                    if line.count('__main__'):
                        return(text)

                if line.count('import'):
                    importModule = re.match('from (.+?) import.+', line)
                    if importModule:
                        moduleName = re.sub(
                            '\.', '\/', importModule.group(1))
                        if not (moduleName in processedModules):
                            processedModules.append(moduleName)
                            if moduleName.count(PACKAGE):
                                text = inline_module(
                                    moduleName + '.py', text, processedModules)
                            else:
                                text = text + line
                    else:
                        moduleName = line.replace('import ', '').rstrip()
                        if not (moduleName in processedModules):
                            processedModules.append(moduleName)
                            text = text + line
                else:
                    text = text + line
        return(text)


def run(sourceFile, targetFile):
    try:
        os.remove(BUILD + targetFile)
    except:
        pass
    text = ''
    processedModules = []
    text = (inline_module(sourceFile, text, processedModules))
    with open(BUILD + targetFile, 'w') as f:
        print('Writing "' + BUILD + targetFile + '"...\n')
        f.write(text)


def main():
    os.chdir(SRC)
    run('proofdocx.py', 'yw_proof_docx.py')
    run('proofodt.py', 'yw_proof_odt.py')
    print('Done.')


if __name__ == '__main__':
    main()
