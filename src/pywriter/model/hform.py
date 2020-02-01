"""Support HTML conversion and formatting.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import re


HTML_SCENE_DIVIDER = '* * *'
# To be placed between scene ending and beginning tags.

# Make the generated html file look good in a web browser:

STYLESHEET = '<style type="text/css">\n' + \
    'h1, h2, h3, h4, p {font: 1em monospace; margin: 3em; line-height: 1.5em}\n' + \
    'h1, h2, h3, h4 {text-align: center}\n' +\
    'h1 {letter-spacing: 0.2em; font-style: italic}' + \
    'h1, h2 {font-weight: bold}\n' + \
    'h3 {font-style: italic}\n' + \
    'p.textbody {margin-top:0; margin-bottom:0}\n' + \
    'p.firstlineindent {margin-top:0; margin-bottom:0; text-indent: 1em}\n' + \
    'strong {font-weight:normal; text-transform: uppercase}\n' + \
    '</style>\n'

HTML_HEADER = '<html>\n' + '<head>\n' + \
    '<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>\n' + STYLESHEET + \
    '<title>$bookTitle$</title>\n' + \
    '</head>\n' + '<body>\n'

HTML_FOOTER = '\n</body>\n</html>\n'


def to_yw7(text: str) -> str:
    """Convert html tags to yw7 raw markup. Return a yw7 markup string."""
    text = text.replace('<i>', '[i]')
    text = text.replace('<I>', '[i]')
    text = text.replace('<em>', '[i]')
    text = text.replace('<EM>', '[i]')
    text = text.replace('</i>', '[/i]')
    text = text.replace('</I>', '[/i]')
    text = text.replace('</em>', '[/i]')
    text = text.replace('</EM>', '[/i]')
    text = text.replace('<b>', '[b]')
    text = text.replace('<B>', '[b]')
    text = text.replace('</b>', '[/b]')
    text = text.replace('</B>', '[/b]')
    text = text.replace('</strong><', '[/b]')
    text = text.replace('</STRONG>', '[/b]')
    text = text.replace('\n', ' ')
    text = text.replace('\r', ' ')
    text = text.replace('\t', ' ')

    text = re.sub('<em.+?>', '[i]', text)
    text = re.sub('<EM.+?>', '[i]', text)
    text = re.sub('<strong.+?>', '[b]', text)
    text = re.sub('<STRONG.+?>', '[b]', text)

    text = text.replace('[/b][b]', '')
    text = text.replace('[/i][i]', '')

    while '  ' in text:
        text = text.replace('  ', ' ')

    return text


def to_html(text: str) -> str:
    """Convert yw7 raw markup to html. Return a html string."""
    try:
        text = text.replace('\n', '</p>\n<p class="firstlineindent">')
        text = text.replace('[i]', '<em>')
        text = text.replace('[/i]', '</em>')
        text = text.replace('[b]', '<strong>')
        text = text.replace('[/b]', '</strong>')
        text = re.sub('\<p(.+?)\>\<\/p\>', '<p\g<1>><br></p>', text)

    except:
        pass

    return text


def strip_markup(text: str) -> str:
    """Strip yw7 raw markup. Return a plain text string."""
    try:
        text = text.replace('[i]', '')
        text = text.replace('[/i]', '')
        text = text.replace('[b]', '')
        text = text.replace('[/b]', '')

    except:
        pass

    return text


def read_html_file(filePath: str) -> tuple:
    """Open a html file being encoded utf-8 or ANSI.
    Return a tuple:
    [0] = Message beginning with SUCCESS or ERROR.
    [1] = The file content in a single string. 
    """
    try:
        with open(filePath, 'r', encoding='utf-8') as f:
            text = (f.read())
    except:
        # HTML files exported by a word processor may be ANSI encoded.
        try:
            with open(filePath, 'r') as f:
                text = (f.read())

        except(FileNotFoundError):
            return ('ERROR: "' + filePath + '" not found.', None)

    return ('SUCCESS', text)


if __name__ == '__main__':
    pass
