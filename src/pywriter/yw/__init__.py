"""Modules for reading and writing yWriter project files.

Modules:

yw_file -- Provide a generic class for yWriter project import and export.
yw7_file -- Provide a class for yWriter 7 project import and export.
yw7_new_file -- Provide a class for yWriter 7 project creation.
yw6_file -- Provide a class for yWriter 6 project import and export.
yw5_file -- Provide a class for yWriter 5 project export.
yw5_new_file -- Provide a class for yWriter 5 project creation.

yw_tree_reader -- Provide an abstract strategy class to read yWriter project files.
utf8_tree_reader -- Provide a strategy class to read utf-8 encoded yWriter project files.
ansi_tree_reader -- Provide a strategy class to read ANSI encoded yWriter project files.

yw_project_merger -- Provide a strategy class to merge two yWriter project structures.
yw_project_creator -- Provide a strategy class to create a new yWriter project structure.

yw_tree_builder -- Provide an abstract strategy class to build an xml tree. 
yw7_tree_builder -- Provide a strategy class to build an yWriter 7 xml tree.
yw7_tree_creator -- Provide a strategy class to build a new yWriter 7 xml tree.
yw6_tree_builder -- Provide a strategy class to build an yWriter 6 xml tree.
yw5_tree_builder -- Provide a strategy class to build an yWriter 5 xml tree.
yw5_tree_creator -- Provide a strategy class to build a new yWriter 5 xml tree.

yw_tree_writer -- Provide an abstract strategy class to write yWriter project files.
utf8_tree_writer -- Provide a strategy class to write utf-8 encoded yWriter project files.
ansi_tree_writer -- Provide a strategy class to write ANSI encoded yWriter project files.

yw_postprocessor -- Provide an abstract strategy class to postprocess yWriter project files.
utf8_postprocessor -- Provide a strategy class to postprocess utf-8 encoded yWriter project files.
ansi_postprocessor -- Provide an abstract strategy class to postprocess yWriter project files.
"""
