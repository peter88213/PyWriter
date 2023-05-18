"""Provide a class for ODT exchange document import.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.pywriter_globals import *
from pywriter.odt_r.odt_r_proof import OdtRProof


class OdtRXch(OdtRProof):
    """ODT exchange document reader.

    Import a manuscript with visibly tagged chapters and scenes.
    """
    DESCRIPTION = _('Tagged manuscript for exchange')
    SUFFIX = '_xch'
