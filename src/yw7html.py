""" Export to html.

Read an yWriter7 project file and create a html file.

For further information see https://github.com/peter88213/yWrestler
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys
import xml.etree.ElementTree as ET

SCENE_DIVIDER = '* * *'

# Make the html file look good in a web browser.
HTML_HEADER = '''<html>
<head>
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
    text = text.replace('\n\n', '\n')
    text = text.replace('\n', '</p>\n<p class="firstlineindent">')
    text = text.replace('[i]', '<em>')
    text = text.replace('[/i]', '</em>')
    text = text.replace('[b]', '<strong>')
    text = text.replace('[/b]', '</strong>')
    return(text)


def yw7_to_html(yw7File, htmlFile):
    """ Read .yw7 file and convert scenes to html. """
    scenes = {}
    titles = {}

    tree = ET.parse(yw7File)
    root = tree.getroot()

    for prj in root.iter('PROJECT'):
        bookTitle = prj.find('Title').text

    for scn in root.iter('SCENE'):
        scnID = scn.find('ID').text
        scenes[scnID] = scn.find('SceneContent').text
        titles[scnID] = scn.find('Title').text

    htmlText = HTML_HEADER.replace('$bookTitle$', bookTitle)

    for chp in root.iter('CHAPTER'):
        htmlText = htmlText + '<div id="ChID:' + chp.find('ID').text + '">\n<h2>' + \
            format_chapter_title(chp.find('Title').text) + '</h2>\n'
        scnList = chp.find('Scenes')
        for scn in scnList.findall('ScID'):
            scnID = scn.text
            htmlText = htmlText + '<h4>' + SCENE_DIVIDER + '</h4>\n<div id="ScID:' + scnID +\
                '">\n<p class="textbody"><!-- ' + titles[scnID] + ' -->\n'
            # Insert scene title as html comment.
            htmlText = htmlText + \
                format_yw7(scenes[scnID]) + '</p>\n</div>\n'
        htmlText = htmlText + '</div>\n'
    htmlText = htmlText.replace(
        '</h2>\n<h4>' + SCENE_DIVIDER + '</h4>', '</h2>\n')
    htmlText = htmlText + HTML_FOOTER

    try:
        with open(htmlFile, 'w', encoding='utf-8') as f:
            f.write(htmlText)
    except:
        pass


def main():
    """ Call the functions with command line arguments. """
    try:
        yw7Path = sys.argv[1]
    except:
        print('Syntax: yw7html.py filename.yw7')
        sys.exit(1)

    htmlPath = yw7Path.split('.yw7')[0] + '.html'
    yw7_to_html(yw7Path, htmlPath)


if __name__ == '__main__':
    main()
