"""HtmlExport - Class for html export with templates.

* Merge a novel object's attributes.
* Convert yw7 markup to HTML. 
* Create a template-based html output file.
* This class is generic and contains no templates.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.file.file_export import FileExport


class HtmlExport(FileExport):
    """Abstract yWriter project file exporter representation.
    To be overwritten by subclasses providing report-specific templates.
    """

    DESCRIPTION = 'HTML report'
    EXTENSION = '.html'
    # overwrites Novel.EXTENSION

    def convert_from_yw(self, text):
        """Convert yw7 markup to HTML.
        """
        HTML_REPLACEMENTS = [
            ['\n', '</p>\n<p>'],
            ['[i]', '<em>'],
            ['[/i]', '</em>'],
            ['[b]', '<strong>'],
            ['[/b]', '</strong>'],
            ['<p></p>', '<p><br /></p>'],
            ['/*', '<!--'],
            ['*/', '-->'],
        ]

        try:

            for r in HTML_REPLACEMENTS:
                text = text.replace(r[0], r[1])

        except AttributeError:
            text = ''

        return(text)
