""" Export chapters for proofing.

Read an yWriter7 project file and create a markdown file with scene 
text divided by [ChID:x] and [ScID:y] tags (as known by 
yWriter5 RTF proofing export).

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys
from pywriter import yw7_to_markdown

print('\n*** Export yw7 scenes to (strict) markdown ***')
try:
    yw7Path = sys.argv[1]
except(IndexError):
    yw7Path = input('\nEnter yW7 project filename: ')
mdPath = yw7Path.split('.yw7')[0] + '.md'
print('\nWARNING: This will overwrite "' +
      mdPath + '" (if exists)!')
userConfirmation = input('Continue (y/n)? ')
if userConfirmation in ('y', 'Y'):
    print(yw7_to_markdown(yw7Path, mdPath))
else:
    print('Program abort by user.\n')
input('Press ENTER to continue ...')
