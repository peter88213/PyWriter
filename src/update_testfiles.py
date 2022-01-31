"""Update test files

Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/yW2OO
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os


# documents = f{os.environ['USERPROFILE']}\\Documents'

documents = '../test/data'
pathList = []

for (path, dirs, files) in os.walk(documents):

    for file in files:

        if file == 'proofed.yw7':
            filepath = (f'{path}/{file}').replace('\\', '/')

            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            modified = False
            newlines = []

            for line in lines:

                if '<RTFFile>' in line:
                    modified = True

                else:
                    newlines.append(line)

            if modified:

                with open(filepath, 'w', encoding='utf-8') as f:
                    f.writelines(newlines)

                print(f'{filepath} written\n')

            else:
                print(f'--- {filepath} skipped\n')
