"""Provide a class for ODT "TOC" export document containing all links 
to the part/chapter/scene/character/location/item description documents.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.pywriter_globals import *
from pywriter.odt_w.odt_writer import OdtWriter


class OdtWToc(OdtWriter):
    """ODT "TOC" file writer.

    Export a brief synopsis with chapter titles and scene titles.
    """
    DESCRIPTION = _('Table of contents')
    SUFFIX = '_toc'

    _fileHeader = f'''{OdtWriter._CONTENT_XML_HEADER}<text:p text:style-name="Title">$Title</text:p>
<text:p text:style-name="Subtitle">$AuthorName</text:p>
'''

    _partTemplate = '''<text:h text:style-name="Toc_20_1" text:outline-level="1"><text:bookmark text:name="ChID$ID"/>${Title}</text:h>
<text:p text:style-name="Toc"><text:a xlink:href="../${ProjectName}_parts.odt#ChID:$ID%7Cregion">→ $Description</text:a></text:p>
'''

    _chapterTemplate = '''<text:h text:style-name="Toc_20_2" text:outline-level="2"><text:bookmark text:name="ChID$ID"/>${Title}</text:h>
<text:p text:style-name="Toc"><text:a xlink:href="../${ProjectName}_chapters.odt#ChID:$ID%7Cregion">→ $Description</text:a></text:p>
'''

    _sceneTemplate = '''<text:h text:style-name="Toc_20_3" text:outline-level="3"><text:bookmark text:name="ScID$ID"/>$Title</text:h>
<text:p text:style-name="Toc"><text:a xlink:href="../${ProjectName}_scenes.odt#ScID:$ID%7Cregion">→ $Description</text:a></text:p>
<text:p text:style-name="Toc"><text:a xlink:href="../${ProjectName}_manuscript.odt#ScID:$ID%7Cregion">→ $Manuscript</text:a></text:p>
'''

    _characterSectionHeading = f'<text:h text:style-name="Toc_20_1" text:outline-level="1">{_("Characters")}</text:h>'
    _characterTemplate = '''<text:h text:style-name="Toc_20_2" text:outline-level="2"><text:bookmark text:name="CrID$ID"/>${Title}</text:h>
<text:p text:style-name="Toc"><text:a xlink:href="../${ProjectName}_characters.odt#CrID:$ID%7Cregion">→ $Description</text:a></text:p>
'''
    _locationSectionHeading = '' f'<text:h text:style-name="Toc_20_1" text:outline-level="1">{_("Locations")}</text:h>'
    _locationTemplate = ''
    _itemSectionHeading = f'<text:h text:style-name="Toc_20_1" text:outline-level="1">{_("Items")}</text:h>'
    _itemTemplate = ''

    _fileFooter = OdtWriter._CONTENT_XML_FOOTER

    def _get_sceneMapping(self, scId, sceneNumber, wordsTotal, lettersTotal):
        """Return a mapping dictionary for a scene section.
        
        Positional arguments:
            scId: str -- scene ID.
            sceneNumber: int -- scene number to be displayed.
            wordsTotal: int -- accumulated wordcount.
            lettersTotal: int -- accumulated lettercount.
        
        Extends the superclass method.
        """
        sceneMapping = super()._get_sceneMapping(scId, sceneNumber, wordsTotal, lettersTotal)
        sceneMapping['Manuscript'] = _('Manuscript')
        sceneMapping['Description'] = _('Scene description')
        return sceneMapping

    def _get_chapterMapping(self, chId, chapterNumber):
        """Return a mapping dictionary for a chapter section.
        
        Positional arguments:
            chId: str -- chapter ID.
            chapterNumber: int -- chapter number to be displayed.
        
        Extends the superclass method.
        """
        chapterMapping = super()._get_chapterMapping(chId, chapterNumber)
        if self.novel.chapters[chId].chLevel == 0:
            chapterMapping['Description'] = _('Chapter description')
        else:
            chapterMapping['Description'] = _('Part description')
        return chapterMapping

