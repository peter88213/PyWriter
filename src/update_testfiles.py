"""Update test files

Temporary helper script

Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/yW2OO
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os

find = '''<office:font-face-decls>
  <style:font-face style:name="StarSymbol" svg:font-family="StarSymbol" style:font-charset="x-symbol"/>
  <style:font-face style:name="Courier New" svg:font-family="&apos;Courier New&apos;" style:font-adornments="Standard" style:font-family-generic="modern" style:font-pitch="fixed"/>
   </office:font-face-decls>
'''

replace = '''<office:font-face-decls>
  <style:font-face style:name="StarSymbol" svg:font-family="StarSymbol" style:font-charset="x-symbol"/>
  <style:font-face style:name="Consolas" svg:font-family="Consolas" style:font-adornments="Standard" style:font-family-generic="modern" style:font-pitch="fixed"/>
  <style:font-face style:name="Courier New" svg:font-family="&apos;Courier New&apos;" style:font-adornments="Standard" style:font-family-generic="modern" style:font-pitch="fixed"/>
 </office:font-face-decls>
'''

# documents = f{os.environ['USERPROFILE']}\\Documents'
documents = '../test/data'
pathList = []
for (path, dirs, files) in os.walk(documents):
    for file in files:
        if file == 'content.xml':
            filepath = (f'{path}/{file}').replace('\\', '/')
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
            modified = False
            if find in text:
                modified = True
                text = text.replace(find, replace)
            if modified:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(text)
                print(f'{filepath} written\n')
            else:
                print(f'--- {filepath} skipped\n')
