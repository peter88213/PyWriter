"""Shared modules for template-based document generation.

This is how the file generation from a yWriter project is generally done:
The write method runs through all chapters, scenes, and world building 
elements, such as characters, locations ans items, and fills templates. 

The package's README file contains a list of templates and placeholders:
https://github.com/peter88213/PyWriter/tree/master/src/pywriter/file#readme

Modules:

file_export.py -- Provide a generic class for template-based file export.
filter.py -- Provide a generic filter class for template-based file export.
sc_lc_filter.py -- Provide a scene per location filter class for template-based file export.
sc_cr_filter.py -- Provide a scene per character filter class for template-based file export.
sc_tg_filter.py -- Provide a scene per tag filter class for template-based file export.
sc_it_filter.py -- Provide a scene per item filter class for template-based file export.
sc_vp_filter.py -- Provide a scene per viewpoint filter class for template-based file export.
"""
