[home](index) > pywriter

---

# The pywriter library - Convert yWriter projects

The system is based on the meta-model of a novel, which is also the basis of the yWriter novel writing 
application: 

There is a project tree that branches into chapters and scenes, plus other branches for documenting 
world-building elements such as characters, locations, and items. 

The root of this tree is represented by the Novel class in the 'model' package. This base class also 
contains some elementary methods for file operations. File format-specific subclasses are derived from 
this Novel superclass. For each file format there is a separate package in the PyWriter library.


## Packages

- [model](model) -- Modules for representation of yWriter's meta model.

- [yw](yw) -- Modules for reading and writing yWriter project files.

- [file](file) -- Shared modules for template-based document generation.

- [odf](odf) -- Shared modules for writing Open Document files.

- [odt](odt) -- Modules for writing Open Document text documents.

- [ods](ods) -- Modules for writing Open Document spreadsheet documents.

- [html](html) -- Modules for reading html files.

- [csv](csv) -- Modules for reading and writing csv spreadsheet documents.

- [converter](converter) -- Modules for conversion of Novel subclasses.

- [ui](ui) -- Modules for user interfaces.





