"""Support HTML conversion and formatting.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import re


def to_yw7(text):
    """Convert html tags to yWriter 6/7 raw markup. 
    Return a yw6/7 markup string.
    """

    # Clean up polluted HTML code.

    text = re.sub('</*font.*?>', '', text)
    text = re.sub('</*span.*?>', '', text)
    text = re.sub('</*FONT.*?>', '', text)
    text = re.sub('</*SPAN.*?>', '', text)

    # Put everything in one line.

    text = text.replace('\n', ' ')
    text = text.replace('\r', ' ')
    text = text.replace('\t', ' ')

    while '  ' in text:
        text = text.replace('  ', ' ').rstrip().lstrip()

    # Replace HTML tags by yWriter markup.

    text = text.replace('<i>', '[i]')
    text = text.replace('<I>', '[i]')
    text = text.replace('</i>', '[/i]')
    text = text.replace('</I>', '[/i]')
    text = text.replace('</em>', '[/i]')
    text = text.replace('</EM>', '[/i]')
    text = text.replace('<b>', '[b]')
    text = text.replace('<B>', '[b]')
    text = text.replace('</b>', '[/b]')
    text = text.replace('</B>', '[/b]')
    text = text.replace('</strong>', '[/b]')
    text = text.replace('</STRONG>', '[/b]')
    text = re.sub('<em.*?>', '[i]', text)
    text = re.sub('<EM.*?>', '[i]', text)
    text = re.sub('<strong.*?>', '[b]', text)
    text = re.sub('<STRONG.*?>', '[b]', text)

    # Remove orphaned tags.

    text = text.replace('[/b][b]', '')
    text = text.replace('[/i][i]', '')
    text = text.replace('[/b][b]', '')

    return text


def strip_markup(text):
    """Strip yWriter 6/7 raw markup. Return a plain text string."""
    try:
        text = text.replace('[i]', '')
        text = text.replace('[/i]', '')
        text = text.replace('[b]', '')
        text = text.replace('[/b]', '')

    except:
        pass

    return text


def read_html_file(filePath):
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
