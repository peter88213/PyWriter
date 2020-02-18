"""OdtPartDesc - Class for OpenDocument xml file operations and parsing.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.model.odtfile import OdtFile
from pywriter.model.odtform import *


class OdtPartDesc(OdtFile):
    """OpenDocument xml manuscript file representation."""

    _ODT_HEADING_MARKERS = ['<text:h text:style-name="Heading_20_3" text:outline-level="3">',
                            '<text:h text:style-name="Heading_20_2" text:outline-level="2">',
                            '<text:h text:style-name="Heading_20_1" text:outline-level="1">']

    _SCENE_DIVIDER = '* * *'
    # To be placed between scene ending and beginning tags.

    def write_content_xml(self):
        """Write part summaries to "content.xml".

        Parts are chapters marked  "Other" and not "Unused" and not "Info".

        Generate "content.xml" containing:
        - book title,
        - part sections containing:
            - the "part" (i.e. chapter) summary.
        Return a message beginning with SUCCESS or ERROR.
        """
        lines = [self._CONTENT_XML_HEADER]

        # Write book title as heading.

        lines.append(self._ODT_HEADING_MARKERS[2] + self.title + '</text:h>')

        for chId in self.srtChapters:

            if self.chapters[chId].chType == 0 and not self.chapters[chId].isUnused:

                if self.chapters[chId].chLevel == 1:

                    # Write heading.

                    lines.append(self._ODT_HEADING_MARKERS[self.chapters[chId].chLevel] + format_chapter_title(
                        self.chapters[chId].title) + '</text:h>')

                    # Write invisible "start chapter" tag.

                    lines.append(
                        '<text:section text:style-name="Sect1" text:name="ChID:' + chId + '">')

                    chapterPrefix = '<text:p text:style-name="Text_20_body">'

                    if self.chapters[chId].summary is not None:

                        # Write chapter summary.

                        lines.append(chapterPrefix +
                                     to_odt(self.chapters[chId].summary) + '</text:p>')

                    else:
                        lines.append(chapterPrefix + '</text:p>')

                    # Write invisible "end chapter" tag.

                    lines.append('</text:section>')

        lines.append(self._CONTENT_XML_FOOTER)
        text = '\n'.join(lines)

        try:
            with open(self._TEMPDIR + '/content.xml', 'w', encoding='utf-8') as f:
                f.write(text)

        except:
            return 'ERROR: Cannot write "content.xml".'

        return 'SUCCESS: Content written to "content.xml"'
