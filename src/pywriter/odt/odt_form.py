"""Support ODT formatting.

Part of the PyWriter project.
Copyright (c) 2020, peter88213
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""


def to_odt(text):
    """Convert yw7 raw markup to odt. Return an xml string."""
    try:
        # process italics and bold markup reaching across linebreaks

        italics = False
        bold = False
        newlines = []
        lines = text.split('\n')
        for line in lines:
            if italics:
                line = '[i]' + line
                italics = False

            if line.count('[i]') > line.count('[/i]'):
                line += '[/i]'
                italics = True

            if bold:
                line = '[b]' + line
                bold = False

            if line.count('[b]') > line.count('[/b]'):
                line += '[/b]'
                bold = True

            newlines.append(line)

        text = '\n'.join(newlines)
        text = text.rstrip().replace(
            '\n', '</text:p>\n<text:p text:style-name="First_20_line_20_indent">')
        text = text.replace(
            '[i]', '<text:span text:style-name="Emphasis">')
        text = text.replace('[/i]', '</text:span>')
        text = text.replace(
            '[b]', '<text:span text:style-name="Strong_20_Emphasis">')
        text = text.replace('[/b]', '</text:span>')
        text = text.replace('&', '&amp;')

    except:
        pass

    return text


if __name__ == '__main__':
    pass
