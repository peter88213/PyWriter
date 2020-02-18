"""Support ODT formatting.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""


def format_chapter_title(text):
    """Fix auto-chapter titles for non-English """
    text = text.replace('Chapter ', '')
    return text


def to_odt(text):
    """Convert yw7 raw markup to odt. Return an xml string."""
    try:
        text = text.replace(
            '\n', '</text:p>\n<text:p text:style-name="First_20_line_20_indent">')
        text = text.replace(
            '[i]', '<text:span text:style-name="Emphasis">')
        text = text.replace('[/i]', '</text:span>')
        text = text.replace(
            '[b]', '<text:span text:style-name="Strong_20_Emphasis">')
        text = text.replace('[/b]', '</text:span>')

    except:
        pass

    return text


if __name__ == '__main__':
    pass
