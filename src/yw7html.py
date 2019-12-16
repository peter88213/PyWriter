""" Export to html.

Read an yWriter7 project file and create a html file.

For further information see https://github.com/peter88213/yWrestler
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys
from ywrestler import yw7_to_html

print('\n*** Export yw7 scenes to html ***')
try:
    yw7Path = sys.argv[1]
except(IndexError):
    yw7Path = input('\nEnter yW7 project filename: ')

htmlPath = yw7Path.split('.yw7')[0] + '.html'

print('\nWARNING: This will overwrite "' +
      htmlPath + '" (if exists)!')
userConfirmation = input('Continue (y/n)? ')

if userConfirmation in ('y', 'Y'):
    print(yw7_to_html(yw7Path, htmlPath))
else:
    print('Program abort by user.\n')
input('Press ENTER to continue ...')
