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


def inline_module(file, package, text, processedModules):
    with open(file, 'r') as f:
        print('Processing "' + file + '"...')
        lines = f.readlines()
        inSuppressedComment = False
        for line in lines:
            if line.count('"""') == 1:
                if file.count(package):
                    if inSuppressedComment:
                        inSuppressedComment = False
                    else:
                        inSuppressedComment = True
                else:
                    text = text + line
            elif not inSuppressedComment:
                if file.count(package):
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
                            if moduleName.count(package):
                                text = inline_module(
                                    moduleName + '.py', package, text, processedModules)
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


def run(sourceFile, targetFile, package):
    try:
        os.remove(targetFile)
    except:
        pass
    text = ''
    processedModules = []
    text = (inline_module(sourceFile, package, text, processedModules))
    with open(targetFile, 'w') as f:
        print('Writing "' + targetFile + '"...\n')
        f.write(text)


def main():
    os.chdir(SRC)
    run('proofdocx.py', BUILD + 'temp.py', 'pywriter')
    run(BUILD + 'temp.py', BUILD + 'yw_proof_docx.py', 'pandoc')
    run('proofodt.py', BUILD + 'temp.py', 'pywriter')
    run(BUILD + 'temp.py', BUILD + 'yw_proof_odt.py', 'pandoc')
    os.remove(BUILD + 'temp.py')
    print('Done.')


if __name__ == '__main__':
    main()
