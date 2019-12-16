""" Export chapters for proofing.

Read an yWriter7 project file and create a markdown file with scene 
text divided by [ChID:x] and [ScID:y] tags (as known by 
yWriter5 RTF proofing export).

For further information see https://github.com/peter88213/yWrestler
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys
import ywrestler

PROGRAM_TITLE = 'Export yw7 scenes to (strict) markdown'


def format_md(text):
    """ Convert yw7 specific markup """
    text = text.replace('\n\n', '\n')
    text = text.replace('\n', '\n\n')
    text = text.replace('[i]', '*')
    text = text.replace('[/i]', '*')
    text = text.replace('[b]', '**')
    text = text.replace('[/b]', '**')
    return(text)


def yw7_to_markdown(yw7File, mdFile):
    """ Read .yw7 file and convert xml to markdown. """

    prj = ywrestler.Project(yw7File)
    prjText = ''
    for chID in prj.sceneLists:
        prjText = prjText + '\\[ChID:' + chID + '\\]\n'
        for scID in prj.sceneLists[chID]:
            prjText = prjText + '\\[ScID:' + scID + '\\]\n'
            prjText = prjText + prj.sceneContents[scID] + '\n'
            prjText = prjText + '\\[/ScID\\]\n'
        prjText = prjText + '\\[/ChID\\]\n'
    prjText = format_md(prjText)

    with open(mdFile, 'w', encoding='utf-8') as f:
        f.write(prjText)

    return('\n' + str(len(prj.sceneContents)) + ' Scenes written to "' + mdFile + '".')


def main():
    print('\n*** ' + PROGRAM_TITLE + ' ***')
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


if __name__ == '__main__':
    main()
