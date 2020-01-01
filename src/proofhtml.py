"""Import and export ywriter7 scenes for proofing. 

Proof reading file format = html with visible chapter and scene tags

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys
from pywriter.proof.proofconsole import ProofConsole

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


class MyHtmlConverter(ProofConsole):

    def postprocess(self):
        with open(self.documentPath, 'r') as f:
            text = f.read()
            text = text.replace(
                '<p>[', '<p class="tag">[')
            text = text.replace(']</p>\n<p>', ']</p>\n<p class="textbody">')
            text = text.replace('<p>', '<p class="firstlineindent">')
            text = HTML_HEADER.replace(
                '$bookTitle$', self.yw7File.title) + text + HTML_FOOTER
        with open(self.documentPath, 'w') as f:
            f.write(text)


def run(sourcePath, silentMode=True):
    myConverter = MyHtmlConverter(sourcePath, 'html', silentMode)


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]
    except:
        print(__doc__)
        sys.exit(1)

    run(sourcePath, False)
