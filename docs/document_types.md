# Document types

The document types are recognized by a suffix added to the yWriter project name.

_Example_ 

- yWriter project file name = `normal.yw7`
- Exported manuscript file name = `normal_manuscript.odt`
- Manuscript file name to import = `normal_manuscript.html`

## General

-   [Document language](#document-language)

## Export from yWriter

### Generate ODT (text document)

-   [Export chapters and scenes](#export-chapters-and-scenes) -- no suffix
-   [Export chapters and scenes for proof reading](#export-chapters-and-scenes-for-proof-reading) -- suffix = `_proof`
-   [Export manuscript with chapter and scene sections](#export-manuscript-with-chapter-and-scene-sections) -- suffix = `_manuscript`
-   [Export scene descriptions](#export-scene-descriptions) -- suffix = `_scenes`
-   [Export chapter descriptions](#export-chapter-descriptions) -- suffix = `_chapters`
-   [Export part descriptions](#export-part-descriptions) -- suffix = `_partst`
-   [Export character descriptions](#export-character-descriptions) -- suffix = `_characters`
-   [Export location descriptions](#export-location-descriptions) -- suffix = `_locations`
-   [Export item descriptions](#export-item-descriptions) -- suffix = `_items`
-   [Export cross reference](#export-cross-reference) -- suffix = `_xref`
-   [Export brief synopsis](#export-brief-synopsis) -- suffix = `_brf_synopsis`
-   [Export Notes chapters](#export-notes-chapters) -- suffix = `_notes`
-   [Export Todo chapters](#export-todo-chapters) -- suffix = `_todo`


### Generate ODS (spreadsheet document)

-   [Export character list](#export-character-list) -- suffix = `_charlist`
-   [Export location list](#export-location-list) -- suffix = `_loclist`
-   [Export item list](#export-item-list) -- suffix = `_itemlist`
-   [Export scene list](#export-scene-list) -- suffix = `_scenelist`

## Import to an existing yWriter project

### Source: ODT file (text document)

-   [Import chapters and scenes for proof reading](#import-chapters-and-scenes-for-proof-reading) -- suffix = `_proof`
-   [Import manuscript with chapter and scene sections](#import-manuscript-with-chapter-and-scene-sections) -- suffix = `_manuscript`
-   [Import scene descriptions](#import-scene-descriptions) -- suffix = `_scenes`
-   [Import chapter descriptions](#import-chapter-descriptions) -- suffix = `_chapters`
-   [Import part descriptions](#import-part-descriptions) -- suffix = `_partst`
-   [Import character descriptions](#import-character-descriptions) -- suffix = `_characters`
-   [Import location descriptions](#import-location-descriptions) -- suffix = `_locations`
-   [Import item descriptions](#import-item-descriptions) -- suffix = `_items`

### Source: ODS file (spreadsheet document)

-   [Import character list](#import-character-list) -- suffix = `_charlist`
-   [Import location list](#import-location-list) -- suffix = `_loclist`
-   [Import item list](#import-item-list) -- suffix = `_itemlist`
-   [Import scene list](#import-scene-list) -- suffix = `_scenelist`
-   [Import plot list](#import-plot-list) -- suffix = `_plotlist`

## Create a new yWriter project

### Source: ODT file (text document)

-   [Import work in progress](#import-work-in-progress) -- no suffix
-   [Import outline](#import-outline) -- no suffix


------------------------------------------------------------------------

## General

### Document language

ODF documents are generally assigned a language that determines spell checking and country-specific character substitutions. In addition, Office Writer lets you assign text passages to languages other than the document language to mark foreign language usage or to suspend spell checking. 

#### Document overall

- If a document language (Language code acc. to ISO 639-1 and country code acc. to ISO 3166-2) is detected in the source document during conversion to yw7 format, these codes are set as yWriter project variables. 

- If language code and country code exist as project variables during conversion from yw7 format, they are inserted into the generated ODF document. 

- If no language and country code exist as project variables when converting from yw7 format, language and country code from the operating system settings are entered into the generated ODF document. 

- The language and country codes are checked superficially. If they obviously do not comply with the ISO standards, they are replaced by the values for "No language". These are:
    - Language = zxx
    - Country = none

#### Text passages in scenes

If text markups for other languages are detected during conversion to the yw7 format, they are converted and transferred to the yWriter scene. 

This then looks like this, for example:

`xxx xxxx [lang=en-AU]yyy yyyy yyyy[/lang=en-AU] xxx xxx` 

To prevent these text markups from interfering with yWriter, they are automatically set as project variables in such a way that yWriter interprets them as HTML instructions during document export. 

For the example shown above, the project variable definition for the opening tag looks like this: 

- *Variable Name:* `lang=en-AU` 
- *Value/Text:* `<HTM <SPAN LANG="en-AU"> /HTM>`

The point of this is that such language assignments are preserved even after multiple conversions in both directions, so they are always effective for spell checking in the ODT document.


[Top of page](#top)


## Export chapters and scenes

Write yWriter 7 chapters and scenes into a new OpenDocument
text document (odt).

-   The document is placed in the same folder as the project.
-   Document's **filename**: `<project name>.odt`.
-   Only "normal" chapters and scenes are exported. Chapters and
    scenes marked "unused", "todo" or "notes" are not exported.
-   Only scenes that are intended for RTF export in yWriter will be
    exported.
-   Scenes beginning with `<HTML>` or `<TEX>` are not exported.
-   Comments in the text bracketed with slashes and asterisks (like
    `/* this is a comment */`) are converted to author's comments.
-   yWriter comments with special marks (like `/*@en this is an endnote. */`) are converted into footnotes or endnotes. Markup:
    - `@fn*` -- simple footnote, marked with an astersik
    - `@fn` -- numbered footnote, marked with a number
    - `@en` -- endnote (always numbered)  
-   Interspersed HTML, TEX, or RTF commands are removed.
-   Gobal variables and project variables are not resolved.
-   Part titles appear as first level heading.
-   Chapter titles appear as second level heading.
-   Scenes are separated by `* * *`. The first line is not
    indented.
-   Starting from the second paragraph, paragraphs begin with
    indentation of the first line.
-   Paragraphs starting with `> ` are formatted as quotations.
-   Scenes marked "attach to previous scene" appear like
    continuous paragraphs.
-   Text markup: Bold and italics are supported. Other highlighting such
    as underline and strikethrough are lost.


[Top of page](#top)

------------------------------------------------------------------------

## Export chapters and scenes for proof reading

Write yWriter 7 chapters and scenes into a new OpenDocument
text document (odt) with scene markers. File name suffix is
`_proof`.

-   Only "normal" chapters and scenes are exported. Chapters and
    scenes marked "unused", "todo" or "notes" are not exported.
-   Scenes beginning with `<HTML>` or `<TEX>` are not exported.
-   Interspersed HTML, TEX, or RTF commands are taken over unchanged.
-   The document contains scene `[ScID:y]` markers. **Do not touch lines
    containing the markers** if you want to be able to write the
    document back to *yw7* format.
-   The document contains chapter and scene headings. However, changes will not be written back.
-   Chapters and scenes can neither be rearranged nor deleted. 
-   When editing the document, you can split scenes by inserting headings or a scene divider:
    -   *Heading 1* → New part title. Optionally, you can add a description, separated by `|`.
    -   *Heading 2* → New chapter title. Optionally, you can add a description, separated by `|`.
    -   `###` → Scene divider. Optionally, you can append the 
        scene title to the scene divider. You can also add a description, separated by `|`.
    -   **Note:** Export documents with split scenes from *Writer* to yw7 not more than once.      
-   Text markup: Bold and italics are supported. Other highlighting such
    as underline and strikethrough are lost.


[Top of page](#top)

------------------------------------------------------------------------

## Export manuscript with chapter and scene sections

Write yWriter 7 chapters and scenes into a new OpenDocument
text document (odt) with invisible chapter and scene sections (to be
seen in the Navigator). File name suffix is `_manuscript`.

-   Only "normal" chapters and scenes are exported. Chapters and
    scenes marked "unused", "todo" or "notes" are not exported.
-   Part titles appear as first level headings.
-   Chapter titles appear as second level headings.
-   Scene titles appear as third level entries in the Navigator. The headings themselves are invisible.
-   Scenes beginning with `<HTML>` or `<TEX>` are not exported.
-   Comments in the text bracketed with slashes and asterisks (like
    `/* this is a comment */`) are converted to author's comments.
-   Interspersed HTML, TEX, or RTF commands for yWriter are taken over unchanged.
-   Gobal variables and project variables from yWriter are not resolved.
-   Chapters and scenes can neither be rearranged nor deleted.
-   With *OpenOffice/LibreOffice Writer*, you can split scenes by inserting headings or a scene divider:
    -  *Heading 1* → New part title. Optionally, you can add a description, separated by `|`.
    -  *Heading 2* → New chapter title. Optionally, you can add a description, separated by `|`.
    -  `###` → Scene divider. Optionally, you can append the 
       scene title to the scene divider. You can also add a description, separated by `|`.
    - **Note:** Export documents with split scenes from *Writer* to yw7 not more than once.      
-   Paragraphs starting with `> ` are formatted as quotations.
-   Text markup: Bold and italics are supported. Other highlighting such
    as underline and strikethrough are lost.

[Top of page](#top)

------------------------------------------------------------------------

## Export scene descriptions

Generate a new OpenDocument text document (odt) containing chapter
titles and scene descriptions that can be edited and written back to
yWriter format. File name suffix is
`_scenes`.

[Top of page](#top)

------------------------------------------------------------------------

## Export chapter descriptions

Generate a new OpenDocument text document (odt) containing chapter
titles and chapter descriptions that can be edited and written back to
yWriter format. File name suffix is
`_chapters`.

**Note:** Doesn't apply to chapters marked
`This chapter begins a new section` in yWriter.

[Top of page](#top)

------------------------------------------------------------------------

## Export part descriptions

Generate a new OpenDocument text document (odt) containing part titles
and part descriptions that can be edited and written back to yWriter
format. File name suffix is
`_parts`.

**Note:** Applies only to chapters marked
`This chapter  begins a new section` in yWriter.

[Top of page](#top)

------------------------------------------------------------------------

## Export character descriptions

Generate a new OpenDocument text document (odt) containing
character descriptions, bio, goals, and notes that can be edited in Office
Writer and written back to yWriter format. File name suffix is
`_characters`.

[Top of page](#top)

------------------------------------------------------------------------

## Export location descriptions

Generate a new OpenDocument text document (odt) containing
location descriptions that can be edited in Office Writer and written
back to yWriter format. File name suffix is `_locations`.

[Top of page](#top)

------------------------------------------------------------------------

## Export item descriptions

Generate a new OpenDocument text document (odt) containing
item descriptions that can be edited in Office Writer and written back
to yWriter format. File name suffix is `_items`.

[Top of page](#top)

------------------------------------------------------------------------

## Export cross reference

Generate a new OpenDocument text document (odt) containing
navigable cross references. File name suffix is `_xref`. The cross
references are:

-   Scenes per character,
-   scenes per location,
-   scenes per item,
-   scenes per tag,
-   characters per tag,
-   locations per tag,
-   items per tag.

[Top of page](#top)

------------------------------------------------------------------------

## Export brief synopsis

Generate a brief synopsis with chapter and scenes titles. File name
suffix is `_brf_synopsis`.

-   Only "normal" chapters and scenes are exported. Chapters and
    scenes marked "unused", "todo" or "notes" are not exported.
-   Only scenes that are intended for RTF export in yWriter will be
    exported.
-   Titles of scenes beginning with `<HTML>` or `<TEX>` are not exported.
-   Chapter titles appear as first level heading if the chapter is
    marked as beginning of a new section in yWriter. Such headings are
    considered as "part" headings.
-   Chapter titles appear as second level heading if the chapter is not
    marked as beginning of a new section. Such headings are considered
    as "chapter" headings.
-   Scene titles appear as plain paragraphs.

[Top of page](#top)

------------------------------------------------------------------------

## Export Notes chapters

Write yWriter 7 "Notes" chapters with child scenes into a new 
OpenDocument text document (odt) with invisible chapter and scene 
sections (to be seen in the Navigator). File name suffix is `_notes`.

-   Comments within scenes are written back as scene titles
    if surrounded by `~`.
-   Chapters and scenes can neither be rearranged nor deleted.
-   With *OpenOffice/LibreOffice Writer*, you can split scenes by inserting headings or a scene divider:
    -  *Heading 1* → New part title. Optionally, you can add a description, separated by `|`.
    -  *Heading 2* → New chapter title. Optionally, you can add a description, separated by `|`.
    -  `###` → Scene divider. Optionally, you can append the 
       scene title to the scene divider. You can also add a description, separated by `|`.
    - **Note:** Export documents with split scenes from *Writer* to yw7 not more than once.      
-   Paragraphs starting with `> ` are formatted as quotations.
-   Text markup: Bold and italics are supported. Other highlighting such
    as underline and strikethrough are lost.

[Top of page](#top)

------------------------------------------------------------------------

## Export Todo chapters

Write yWriter 7 "Todo" chapters with child scenes into a new 
OpenDocument text document (odt) with invisible chapter and scene 
sections (to be seen in the Navigator). File name suffix is `_todo`.

-   Comments within scenes are written back as scene titles
    if surrounded by `~`.
-   Chapters and scenes can neither be rearranged nor deleted.
-   With *OpenOffice/LibreOffice Writer*, you can split scenes by inserting headings or a scene divider:
    -  *Heading 1* → New part title. Optionally, you can add a description, separated by `|`.
    -  *Heading 2* → New chapter title. Optionally, you can add a description, separated by `|`.
    -  `###` → Scene divider. Optionally, you can append the 
       scene title to the scene divider. You can also add a description, separated by `|`.
    - **Note:** Export documents with split scenes from *Writer* to yw7 not more than once.      
-   Paragraphs starting with `> ` are formatted as quotations.
-   Text markup: Bold and italics are supported. Other highlighting such
    as underline and strikethrough are lost.

[Top of page](#top)

------------------------------------------------------------------------

## Export character list

Generate a new OpenDocument spreadsheet (ods) containing a
character list that can be edited in Office Calc and written back to
yWriter format. File name suffix is `_charlist`.

You may change the sort order of the rows. You may also add or remove
rows. New entities must get a unique ID.

[Top of page](#top)

------------------------------------------------------------------------

## Export location list

Generate a new OpenDocument spreadsheet (ods) containing a
location list that can be edited in Office Calc and written back to
yWriter format. File name suffix is `_loclist`.

You may change the sort order of the rows. You may also add or remove
rows. New entities must get a unique ID.

[Top of page](#top)

------------------------------------------------------------------------

## Export item list

Generate a new OpenDocument spreadsheet (ods) containing an
item list that can be edited in Office Calc and written back to yWriter
format. File name suffix is `_itemlist`.

You may change the sort order of the rows. You may also add or remove
rows. New entities must get a unique ID.

[Top of page](#top)

------------------------------------------------------------------------

## Export scene list

Generate a new OpenDocument spreadsheet (ods) listing the following:

- Hyperlink to the manuscript's scene section
- Scene title
- Scene description
- Tags
- Scene notes
- A/R
- Goal
- Conflict
- Outcome
- Sequential scene number
- Words total
- Rating 1
- Rating 2
- Rating 3
- Rating 4
- Word count
- Letter count
- Status
- Characters
- Locations
- Items

Only "normal" scenes that would be exported as RTF in yWriter get a 
row in the scene list. Scenes of the "Unused", "Notes", or "ToDo" 
type are omitted.
Scenes beginning with `<HTML>` or `<TEX>` are omitted.

File name suffix is `_scenelist`.

[Top of page](#top)

------------------------------------------------------------------------

## Import scene list

The following columns can be written back to the yWriter project:

- Title
- Description
- Tags (comma-separated)
- Scene notes
- A/R (action/reaction scene)
- Goal
- Conflict
- Outcome
- Rating 1
- Rating 2
- Rating 3
- Rating 4
- Status ('Outline', 'Draft', '1st Edit', '2nd Edit', 'Done')

[Top of page](#top)

------------------------------------------------------------------------


