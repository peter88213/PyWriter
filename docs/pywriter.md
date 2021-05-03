[home](index)

- - -

# pywriter - A library for yWriter project conversion.

The system is based on the meta-model of a novel, which is also the basis of the yWriter novel writing 
application: 

There is a project tree that branches into chapters and scenes, plus other branches for documenting 
world-building elements such as characters, locations, and items. 

The root of this tree is represented by the Novel class in the 'model' package. This base class also 
contains some elementary methods for file operations. File format-specific subclasses are derived from 
this Novel superclass. For each file format there is a separate package in the PyWriter library.


## Package structure

[model](model) - The novel meta-model

--[yw](yw) - Read and write yWriter projects

--[file](file) - Template-based file generation

----[odf](odf) - Open document format base class

------[odt](odt) - Write text documents

------[ods](ods) - Write spreadsheet documents

----[html](html) - Read text documents

----[csv](csv) - Read spreadsheet documents

--[md](md) - Read and write Markdown formatted documents

[converter](converter) - Convert from one file format to another



