"""Provide a class for html invisibly tagged part descriptions import.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from pywriter.html.html_chapterdesc import HtmlChapterDesc


class HtmlPartDesc(HtmlChapterDesc):
    """HTML part summaries file representation.

    Import a very brief synopsis with invisibly tagged part descriptions.
    """

    DESCRIPTION = 'Part descriptions'
    SUFFIX = '_parts'
