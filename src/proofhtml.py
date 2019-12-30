"""Import and export ywriter7 scenes for proofing. 

Proof reading file format = html with visible chapter and scene tags

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys
import os
from pywriter.documentconverter import DocumentConverter

STYLESHEET = '<style type="text/css">\n' + \
    'h1, h2, h3, h4, p {font: 1em monospace; margin: 3em; line-height: 1.5em}\n' + \
    'h1, h2, h3, h4 {text-align: center}\n' +\
    'h1 {letter-spacing: 0.5em; font-style: italic}' + \
    'h1, h2 {font-weight: bold}\n' + \
    'h3 {font-style: italic}\n' + \
    'p.tag {font-size:x-small}\n' + \
    'p.textbody {margin-top:0; margin-bottom:0}\n' + \
    'p.firstlineindent {margin-top:0; margin-bottom:0; text-indent: 1em}\n' + \
    'strong {font-weight:normal; text-transform: uppercase}\n' + \
    '</style>\n'
# Make the generated html file look good in a web browser.

HTML_HEADER = '<html>\n' + '<head>\n' + \
    '<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>\n' + \
    STYLESHEET + \
    '<title>$bookTitle$</title>\n' + \
    '</head>\n' + '<body>\n'

HTML_FOOTER = '\n</body>\n</html>\n'


class MyHtmlConverter(DocumentConverter):

    def __init__(self, yw7File, htmlFile, silentMode=True):
        DocumentConverter.__init__(self, yw7File, htmlFile)
        self.silentMode = silentMode

    def confirm_overwrite(self, file):
        if not self.silentMode:
            print('\nWARNING: This will overwrite "' +
                  file + '"!')
            userConfirmation = input('Continue (y/n)? ')
            if not userConfirmation in ('y', 'Y'):
                print('Program abort by user.\n')
                input('Press ENTER to continue ...')
                sys.exit(1)


def run(sourcePath, silentMode=True):
    """ File conversion for proofreading. """
    sourceFile = os.path.split(sourcePath)
    pathToSource = sourceFile[0]
    if pathToSource:
        pathToSource = pathToSource + '/'

    if sourceFile[1].count('.yw7'):
        yw7File = pathToSource + sourceFile[1]

        htmlFile = pathToSource + \
            sourceFile[1].split('.yw7')[0] + '.html'
        myConverter = MyHtmlConverter(yw7File, htmlFile, silentMode)
        print('\n*** Export yWriter7 scenes to HTML ***')
        print('Project: "' + yw7File + '"')
        print(myConverter.yw7_to_document())
        with open(htmlFile, 'r') as f:
            text = f.read()
            text = text.replace(
                '<p>[', '<p class="tag">[')
            text = text.replace(']</p>\n<p>', ']</p>\n<p class="textbody">')
            text = text.replace('<p>', '<p class="firstlineindent">')
            text = HTML_HEADER.replace(
                '$bookTitle$', myConverter.yw7Prj.title) + text + HTML_FOOTER
        with open(htmlFile, 'w') as f:
            f.write(text)

    elif sourceFile[1].count('.html'):
        htmlFile = pathToSource + sourceFile[1]
        yw7File = pathToSource + \
            sourceFile[1].split('.html')[0] + '.yw7'
        myConverter = MyHtmlConverter(yw7File, htmlFile, silentMode)
        print('\n*** Import yWriter7 scenes from HTML ***')
        print('Proofed scenes in "' + htmlFile + '"')
        print(myConverter.document_to_yw7())

    else:
        print('Input file must be .yw7 or .html type.')

    if not silentMode:
        input('Press ENTER to continue ...')


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]
    except:
        print(__doc__)
        sys.exit(1)

    run(sourcePath, False)
