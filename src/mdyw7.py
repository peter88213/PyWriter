""" Import proofed chapters. 

Read a markdown file with scene text divided by [ChID:x] and [ScID:y] tags 
(as known by yWriter5 RTF proofing export) and replace the scenes
in an yw7 project file.

For further information see https://github.com/peter88213/yWrestler
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys
from pywriter import markdown_to_yw7

print('\n*** Import yw7 scenes from (strict) markdown ***')
try:
    mdPath = sys.argv[1]
except:
    mdPath = input('\nEnter md filename: ')
yw7Path = mdPath.split('.md')[0] + '.yw7'
print('\nWARNING: This will overwrite "' +
      yw7Path + '"!')
userConfirmation = input('Continue (y/n)? ')
if userConfirmation in ('y', 'Y'):
    print(markdown_to_yw7(mdPath, yw7Path))
else:
    print('Program abort by user.\n')
input('Press ENTER to continue ...')
