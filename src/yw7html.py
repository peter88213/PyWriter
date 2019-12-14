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
</head>
<body>
'''

HTML_FOOTER = '''
</body>
</html>
'''


def format_scene(text):
    """ Convert yw7 raw markup """
    text = text.replace('\n\n', '\n')
    text = text.replace('\n', "</p>\n<p class='firstlineindent'>")
    text = text.replace('[i]', '<em>')
    text = text.replace('[/i]', '</em>')
    text = text.replace('[b]', '<strong>')
    text = text.replace('[/b]', '</strong>')
    return(text)


def format_chapter_title(text):
    """ Fix auto-chapter titles for non-English """
    text = text.replace('Chapter ', '')
    return(text)


def yw7_to_html(yw7File):
    """ Read .yw7 file and convert scenes to html. """
    tree = ET.parse(yw7File)
    root = tree.getroot()  # all item attributes

    scenes = {}
    titles = {}
    for scn in root.iter('SCENE'):
        scnID = scn.find('ID').text
        scenes[scnID] = scn.find('SceneContent').text
        titles[scnID] = scn.find('Title').text

    htmlText = HTML_HEADER
    for chp in root.iter('CHAPTER'):
        htmlText = htmlText + '<h2>' + \
            format_chapter_title(chp.find('Title').text) + '</h2>\n'
        scnList = chp.find('Scenes')
        for scn in scnList.findall('ScID'):
            scnID = scn.text
            htmlText = htmlText + '<h4>' + SCENE_DIVIDER + '</h4>\n' + \
                '<!-- ' + titles[scnID] + " -->\n<p class='textbody'>"
            # Insert scene title as html comment.
            htmlText = htmlText + format_scene(scenes[scnID]) + '</p>\n'
    htmlText = htmlText.replace(
        '</h2>\n<h4>' + SCENE_DIVIDER + '</h4>', '</h2>\n')
    return(htmlText + HTML_FOOTER)


def write_html(htmlText, htmlPath):
    """ Create .html file. """
    with open(htmlPath, 'w') as f:
        f.write(htmlText)


def main():
    """ Call the functions with command line arguments. """
    try:
        yw7Path = sys.argv[1]
    except:
        print('Syntax: yw7html.py filename.yw7')
        sys.exit(1)

    prjText = yw7_to_html(yw7Path)
    # Read .yw7 file and convert scenes to html.
    htmlPath = yw7Path.split('.yw7')[0] + '.html'
    write_html(prjText, htmlPath)
    # Create .html file.


if __name__ == '__main__':
    main()
