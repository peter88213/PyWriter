""" Export to html.

Read an yWriter7 project file and create a html file.

For further information see https://github.com/peter88213/yWrestler
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys
import ywrestler

PROGRAM_TITLE = 'Export yw7 scenes to html'

SCENE_DIVIDER = '* * *'

# Make the html file look good in a web browser.
HTML_HEADER = '''<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<style type='text/css'>
h2, h4, p {font: 1em monospace; margin: 3em; line-height: 1.5em}
p.textbody {margin-top:0; margin-bottom:0}
p.firstlineindent {margin-top:0; margin-bottom:0; text-indent: 1em}
h2 {font-weight: bold}
h2, h4 {text-align: center}
strong {font-weight:normal; text-transform: uppercase}
</style>
<title>$bookTitle$</title>
</head>
<body>
'''

HTML_FOOTER = '''
</body>
</html>
'''


def format_chapter_title(text):
    """ Fix auto-chapter titles for non-English """
    text = text.replace('Chapter ', '')
    return(text)


def format_yw7(text):
    """ Convert yw7 raw markup """
    try:
        text = text.replace('\n\n', '\n')
        text = text.replace('\n', '</p>\n<p class="firstlineindent">')
        text = text.replace('[i]', '<em>')
        text = text.replace('[/i]', '</em>')
        text = text.replace('[b]', '<strong>')
        text = text.replace('[/b]', '</strong>')
    except:
        pass
    return(text)


def yw7_to_html(yw7File, htmlFile):
    """ Read .yw7 file and convert sceneContents to html. """

    yw7Project = ywrestler.Project(yw7File)

    sceneTitles = yw7Project.get_scenes()[0]
    sceneContents = yw7Project.get_scenes()[1]
    chapterTitles = yw7Project.get_chapters()[0]
    sceneLists = yw7Project.get_chapters()[1]

    htmlText = HTML_HEADER.replace('$bookTitle$', yw7Project.get_title())

    for chID in chapterTitles:
        htmlText = htmlText + '<div id="ChID:' + chID + '">\n<h2>' + \
            format_chapter_title(chapterTitles[chID]) + '</h2>\n'
        for scID in sceneLists[chID]:
            htmlText = htmlText + '<h4>' + SCENE_DIVIDER + '</h4>\n<div id="ScID:' + scID +\
                '">\n<p class="textbody"><!-- ' + sceneTitles[scID] + ' -->\n'
            # Insert scene title as html comment.
            try:
                htmlText = htmlText + \
                    format_yw7(sceneContents[scID]) + '</p>\n</div>\n'
            except:
                pass
        htmlText = htmlText + '</div>\n'
    htmlText = htmlText.replace(
        '</h2>\n<h4>' + SCENE_DIVIDER + '</h4>', '</h2>\n')
    htmlText = htmlText + HTML_FOOTER

    try:
        with open(htmlFile, 'w', encoding='utf-8') as f:
            f.write(htmlText)
    except(PermissionError):
        return('\nERROR: ' + htmlFile + '" is write protected.')

    return('\n' + str(len(sceneContents)) + ' Scenes written to "' + htmlFile + '".')


def main():
    print('\n*** ' + PROGRAM_TITLE + ' ***')
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


if __name__ == '__main__':
    main()
