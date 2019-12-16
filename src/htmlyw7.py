""" Import proofed chapters. 

Read a html file divided into ChID:x and ScID:y sections 
and replace the scenes in an yw7 project file.

For further information see https://github.com/peter88213/yWrestler
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys
from ywrestler import html_to_yw7

print('\n*** Import yw7 scenes from html ***')
try:
    htmlPath = sys.argv[1]
except(IndexError):
    htmlPath = input('\nEnter html filename: ')

yw7Path = htmlPath.split('.html')[0] + '.yw7'

print('\nWARNING: This will overwrite "' +
      yw7Path + '"!')
userConfirmation = input('Continue (y/n)? ')
if userConfirmation in ('y', 'Y'):
    print(html_to_yw7(htmlPath, yw7Path))
else:
    print('Program abort by user.\n')
input('Press ENTER to continue ...')
