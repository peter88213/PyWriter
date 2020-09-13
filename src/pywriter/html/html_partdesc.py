"""HtmlPartDesc - Class for html part summary file parsing.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from pywriter.html.html_chapterdesc import HtmlChapterDesc


class HtmlPartDesc(HtmlChapterDesc):
    """HTML file representation of an yWriter project's parts summaries."""

    DESCRIPTION = 'Part descriptions'
    SUFFIX = '_parts'
