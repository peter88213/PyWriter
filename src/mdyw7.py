""" Import proofed chapters. 

Read a markdown file with scene text divided by [ChID:x] and [ScID:y] tags 
(as known by yWriter5 RTF proofing export) and replace the scenes
in an yw7 project file.

For further information see https://github.com/peter88213/yWrestler
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import re
import sys
import ywrestler

PROGRAM_TITLE = 'Import yw7 scenes from (strict) markdown'


def format_yw7(text):
    """ Convert markdown to yw7 raw markup. """
    text = text.replace('\n\n', '\n')
    text = text.replace('\[', '[')
    text = text.replace('\]', ']')
    text = re.sub('\*\*(.+?)\*\*', '[b]\g<1>[/b]', text)
    text = re.sub('\*(.+?)\*', '[i]\g<1>[/i]', text)
    return(text)


def md_to_yw7(mdFile, yw7File):
    """ Convert markdown to xml and replace .yw7 file. """
    try:
        with open(mdFile, 'r', encoding='utf-8') as f:
            text = (f.read())
    except(FileNotFoundError):
        return('\nERROR: "' + mdFile + '" not found.')

    text = format_yw7(text)
    sceneContents = {}
    sceneText = ''
    scID = ''
    lines = text.split('\n')
    for line in lines:
        if line.count('[ChID'):
            pass
        elif line.count('[ScID'):
            scID = re.search('[0-9]+', line).group()
        elif line.count('[/ChID]'):
            pass
        elif line.count('[/ScID]'):
            sceneContents[scID] = sceneText
            sceneText = ''
        else:
            sceneText = sceneText + line + '\n'

    yw7Project = ywrestler.Project(yw7File)

    return(yw7Project.write_scene_contents(sceneContents))


def main():
    print('\n*** ' + PROGRAM_TITLE + ' ***')
    try:
        mdPath = sys.argv[1]
    except:
        mdPath = input('\nEnter md filename: ')

    yw7Path = mdPath.split('.md')[0] + '.yw7'

    print('\nWARNING: This will overwrite "' +
          yw7Path + '" (if exists)!')
    userConfirmation = input('Continue (y/n)? ')
    if userConfirmation in ('y', 'Y'):
        print(md_to_yw7(mdPath, yw7Path))
    else:
        print('Program abort by user.\n')
    input('Press ENTER to continue ...')


if __name__ == '__main__':
    main()
