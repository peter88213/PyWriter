[home](index) > roadmap

- - -

# The pywriter development roadmap

## About versioning

This project uses semantic versioning with three-part numbers.

__Up to v2.16__ , the following applies: 

*  __Major version__  numbers are incremented for changes on the upper architectural level.
*  __Minor version__  numbers are incremented for releases which change the API in any way.
*  __Patch__  numbers are incremented for minor changes and bug fixes which do not change the API. 

__As of v2.12__ , the following applies to the  __minor versions__ :
*  __Even numbers__  indicate releases, published on the  _master_  branch. 
*  __Odd numbers__  are development versions, initially not on the  _master_  branch.

__As of v2.16__ , the following applies:

*  __Major version__  numbers are incremented for API changes which are not backward-compatible.
*  __Minor version__  numbers are incremented for releases which add new, but backward-compatible, API features
*  __Patch__  numbers are incremented for minor changes and bug fixes which do not change the API. 

## Version 1.x: Standalone exporters and importers for proof reading

Standalone exporters and importers to and from office word processors. 

### File formats 

* ODT
* DOCX
* HTML

### Features

#### v1.0

* Export yw7 scenes als markdown (yWriter5 ChID and ScID tags).
* Pandoc wrappers convert markdown to odt, docx or html and vice versa.
* Import proofed scenes from markdown with yWriter5 ChID and ScID tags.
* Invoked via command line / drag and drop.

#### v1.1

* Add a simple GUI to replace the "non silent" console interface such as _confirm overwrite_ and error/success messages by a tkinter window with labels and buttons. 

#### v1.2

* Replace Markdown export/import by a HTML-based solution to make Pandoc use unnecessary.

#### v1.3

* Discontinue the development of the non-Libre/OpenOffice converters.
* Invoke conversion scripts by Explorer context menu.

#### v1.4

* Supported Conversions:
    - yw7 to odt
    - yw7 to csv
    - html to yw7
    - csv to yw7

* Move applications into own repositories.

#### v1.5

* Abandon non-Libre/OpenOffice converters.

#### v1.6

* Support yWriter versions 5, 6, 7:
    - yw5: No processing of scene content; export and import metadata only.
    - yw6: May add some features that are still missing in yw7.

#### v1.7

* Support scene status. 
* Support Characters, Locations, Items.
    - Table via csv export/import.
    - Office document export&import.

#### v1.8
* Provide global constants for the file name suffixes.
* File Classes: Separate "merge" and "write" methods.
* Support plotting, following conventions yet to be defined.
    - Character arcs (using data fields, or tags, or notes).
    - Dramatic structure (using chapter type, or tags, or scene notes).

#### v1.9

* Create a new yw7 file, substituting yWriter7's broken "Import work in progress" feature.

#### v1.10

* Support outline import.

## Version 2.x: Template-based exporters

Standalone exporters and importers to be used by Open/LibreOffice extensions. 

### File formats 

* ODT
* HTML
* CSV
* ODS (as of v2.11)
* Markdown (as of v2.16)

### Features

#### v2.0

* Make file export template-based.

#### v2.5

* Refactor the code: apply design patterns for better maintainability.
* Unify converter classes (same init parameters and convert methods)
* Make YwFile an abstract class with version-dependent subclasses.
* Improve screen output. 

#### v2.6

* Refactor the code: provide different FileFactory subclasses in order to make applications smaller.

#### v2.7

Set a blank line (instead of the three asterisks) as scene divider template.

#### v2.8

Process all yWriter formatting tags.
* Convert underline and strikethrough.
* Discard alignment.
* Discard highlighting.

#### v2.9

Don't support underline and strikethrough anymore.
That is because a real support would require considering nesting and
multi paragraph formatting. That would make everything too complicated,
considering that such formatting is not common in a fictional prose
text.

#### v2.10

Import new and re-ordered characters/locations/items from csv lists.

#### v2.11

Change item/location list export from csv to ods file format.

#### v2.12

Change scene and plot list export from csv to ods file format.

#### v2.14

* Generate cross reference dictionaries (tags, characters, locations, items).
* Export cross references to an odt document.
* Control the template-based exports from the FileExport subclasses.

#### v2.16

* Add Markdown processing.
* Add HtmlExport class.

#### v2.18

* Add real GUI capability while remaining downward compatible.


### Future:

#### Edit the novel structure independently from yWriter

* Write back the whole yWriter project structure.
    - Create a new xml tree when writing back a yWriter project.
    - Add, delete, move chapters.
    - Add, delete, move scenes.
    - Add, delete characters, locations, and items (already implemented as of v2.10).


#### Full LibreOffice/OpenOffice integration

* Data base support:
	- Read/write a LibreOffice/OpenOffice supported data base.
	- Generate Office documents from the data base.



