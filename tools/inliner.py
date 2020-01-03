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
        inHeader = True
        # document parsing always starts in the header
        for line in lines:
            if (inHeader) and line.count('"""') == 1:
                # Beginning or end of a docstring
                if file.count(package):
                    # This is not the root script
                    # so suppress the module's docstring
                    if inSuppressedComment:
                        # docstring ends
                        inSuppressedComment = False
                        inHeader = False
                    else:
                        # docstring begins
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
                    if importModule and importModule.group(1).count(package):
                        moduleName = re.sub(
                            '\.', '\/', importModule.group(1))
                        if not (moduleName in processedModules):
                            processedModules.append(moduleName)
                            text = inline_module(
                                moduleName + '.py', package, text, processedModules)
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
    run('proofdocx.py', BUILD + 'yw_proof_docx.py', 'pywriter')
    run('proofodt.py', BUILD + 'yw_proof_odt.py', 'pywriter')
    print('Done.')


if __name__ == '__main__':
    main()
