"""Provide a base class for ODT documents containing text that is formatted in yWriter.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import re
from pywriter.pywriter_globals import *
from pywriter.odt.odt_file import OdtFile


class OdtFormatted(OdtFile):
    """ODT file representation.

    Provide methods for processing chapters with formatted text.
    """

    def _convert_from_yw(self, text, quick=False):
        """Return text, converted from yw7 markup to target format.
        
        Positional arguments:
            text -- string to convert.
        
        Optional arguments:
            quick -- bool: if True, apply a conversion mode for one-liners without formatting.
        
        Overrides the superclass method.
        """
        if text:
            text = text.replace('&', '&amp;').replace('>', '&gt;').replace('<', '&lt;')
            if quick:
                # Just clean up a one-liner without sophisticated formatting.
                return text

            # process italics and bold markup reaching across linebreaks
            italics = False
            bold = False
            newlines = []
            lines = text.split('\n')
            for line in lines:
                if italics:
                    line = f'[i]{line}'
                    italics = False
                while line.count('[i]') > line.count('[/i]'):
                    line = f'{line}[/i]'
                    italics = True
                while line.count('[/i]') > line.count('[i]'):
                    line = f'[i]{line}'
                line = line.replace('[i][/i]', '')
                if bold:
                    line = f'[b]{line}'
                    bold = False
                while line.count('[b]') > line.count('[/b]'):
                    line = f'{line}[/b]'
                    bold = True
                while line.count('[/b]') > line.count('[b]'):
                    line = f'[b]{line}'
                line = line.replace('[b][/b]', '')
                newlines.append(line)
            text = '\n'.join(newlines).rstrip()

            # Apply odt formating.
            ODT_REPLACEMENTS = [
                ('\n\n', '</text:p>\r<text:p text:style-name="First_20_line_20_indent" />\r<text:p text:style-name="Text_20_body">'),
                ('\n', '</text:p>\r<text:p text:style-name="First_20_line_20_indent">'),
                ('\r', '\n'),
                ('[i]', '<text:span text:style-name="Emphasis">'),
                ('[/i]', '</text:span>'),
                ('[b]', '<text:span text:style-name="Strong_20_Emphasis">'),
                ('[/b]', '</text:span>'),
                ('/*', f'<office:annotation><dc:creator>{self.authorName}</dc:creator><text:p>'),
                ('*/', '</text:p></office:annotation>'),
            ]
            for yw, od in ODT_REPLACEMENTS:
                text = text.replace(yw, od)

            # Remove highlighting, alignment,
            # strikethrough, and underline tags.
                text = re.sub('\[\/*[h|c|r|s|u]\d*\]', '', text)
        else:
            text = ''
        return text

    def _get_text(self):
        """Call all processing methods.
        
        Return a string to be written to the output file.
        Overrides the superclass method.
        """
        lines = self._get_fileHeader()
        lines.extend(self._get_chapters())
        lines.append(self._fileFooter)
        text = ''.join(lines)

        # Set style of paragraphs that start with "> " to "Quotations".
        # This is done here to include the scene openings.
        if '&gt; ' in text:
            quotMarks = ('"First_20_line_20_indent">&gt; ',
                         '"Text_20_body">&gt; ',
                         )
            for quotMark in quotMarks:
                text = text.replace(quotMark, '"Quotations">')
            text = re.sub('"Text_20_body"\>(\<office\:annotation\>.+?\<\/office\:annotation\>)\&gt\; ', '"Quotations">\\1', text)
        return text
