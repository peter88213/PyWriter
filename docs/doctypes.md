[Home](index) > Document types

# Document types

The document types are recognized by a suffix added to the yWriter project name.

_Example_ 

- yWriter project file name = `normal.yw7`
- Exported manuscript file name = `normal_manuscript.odt`
- Manuscript file name to import = `normal_manuscript.html`

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


### Generate ODS (spreadsheet document)

-   [Export character list](#export-character-list) -- suffix = `_charlist`
-   [Export location list](#export-location-list) -- suffix = `_loclist`
-   [Export item list](#export-item-list) -- suffix = `_itemlist`
-   [Export scene list](#export-scene-list) -- suffix = `_scenelist`

## Import to an existing yWriter project

### Source: HTML file (text document)

-   [Import chapters and scenes for proof reading](#import-chapters-and-scenes-for-proof-reading) -- suffix = `_proof`
-   [Import manuscript with chapter and scene sections](#import-manuscript-with-chapter-and-scene-sections) -- suffix = `_manuscript`
-   [Import scene descriptions](#import-scene-descriptions) -- suffix = `_scenes`
-   [Import chapter descriptions](#import-chapter-descriptions) -- suffix = `_chapters`
-   [Import part descriptions](#import-part-descriptions) -- suffix = `_partst`
-   [Import character descriptions](#import-character-descriptions) -- suffix = `_characters`
-   [Import location descriptions](#import-location-descriptions) -- suffix = `_locations`
-   [Import item descriptions](#import-item-descriptions) -- suffix = `_items`

### Source: CSV file (spreadsheet document)

-   [Import character list](#import-character-list) -- suffix = `_charlist`
-   [Import location list](#import-location-list) -- suffix = `_loclist`
-   [Import item list](#import-item-list) -- suffix = `_itemlist`
-   [Import scene list](#import-scene-list) -- suffix = `_scenelist`
-   [Import plot list](#import-plot-list) -- suffix = `_plotlist`

## Create a new yWriter project

### Source: HTML file (text document)

-   [Import work in progress](#import-work-in-progress) -- no suffix
-   [Import outline](#import-outline) -- no suffix


------------------------------------------------------------------------

## Export chapters and scenes

Write yWriter 7 chapters and scenes into a new OpenDocument
text document (odt).

-   The document is placed in the same folder as the yWriter project.
-   Document's **filename**: `<yW project name>.odt`.
-   Text markup: Bold and italics are supported. Other highlighting such
    as underline and strikethrough are lost.
-   Only "normal" chapters and scenes are exported. Chapters and
    scenes marked "unused", "todo" or "notes" are not exported.
-   Only scenes that are intended for RTF export in yWriter will be
    exported.
-   Scenes beginning with <HTML> or <TEX> are not exported.
-   Comments in the text bracketed with slashes and asterisks (like
    `/* this is a comment */`) are converted to author's comments.
-   Interspersed HTML, TEX, or RTF commands are removed.
-   Gobal variables and project variables are not resolved.
-   Chapter titles appear as first level heading if the chapter is
    marked as beginning of a new section in yWriter. Such headings are
    considered as "part" headings.
-   Chapter titles appear as second level heading if the chapter is not
    marked as beginning of a new section. Such headings are considered
    as "chapter" headings.
-   Scene titles appear as navigable comments pinned to the beginning of
    the scene.
-   Usually, scenes are separated by blank lines. The first line is not
    indented.
-   Starting from the second paragraph, paragraphs begin with
    indentation of the first line.
-   Paragraphs starting with `> ` are formatted as quotations.
-   Scenes marked "attach to previous scene" in yWriter appear like
    continuous paragraphs.

[Top of page](#top)

------------------------------------------------------------------------

## Export chapters and scenes for proof reading

Write yWriter 7 chapters and scenes into a new OpenDocument
text document (odt) with chapter and scene markers. File name suffix is
`_proof`.

-   The proof read document is placed in the same folder as the yWriter
    project.
-   Document's filename: `<yW project name>_proof.odt`.
-   Text markup: Bold and italics are supported. Other highlighting such
    as underline and strikethrough are lost.
-   Scenes beginning with <HTML> or <TEX> are not exported.
-   All other chapters and scenes are exported, whether "used" or
    "unused".
-   Interspersed HTML, TEX, or RTF commands are taken over unchanged.
-   The document contains chapter `[ChID:x]` and scene `[ScID:y]`
    markers according to yWriter 5 standard. **Do not touch lines
    containing the markers** if you want to be able to reimport the
    document into yWriter.
-   Chapters and scenes can neither be rearranged nor deleted.
-   Scenes can be split by inserting headings or a scene divider:
    -  *Heading 1* --› New chapter title (beginning a new section).
    -  *Heading 2* --› New chapter title.
    -  `###` --› Scene divider.  Optionally, you can append the 
       scene title to the scene divider.



[Top of page](#top)

------------------------------------------------------------------------

## Export manuscript with chapter and scene sections

Write yWriter 7 chapters and scenes into a new OpenDocument
text document (odt) with invisible chapter and scene sections (to be
seen in the Navigator). File name suffix is `_manuscript`.

-  Only "normal" chapters and scenes are exported. Chapters and
   scenes marked "unused", "todo" or "notes" are not exported.
-  Scenes beginning with <HTML> or <TEX> are not exported.
-  Comments within scenes are written back as scene titles 
   if surrounded by `~`.
-  Chapters and scenes can neither be rearranged nor deleted.
-  Scenes can be split by inserting headings or a scene divider:
    -  *Heading 1* --› New chapter title (beginning a new section).
    -  *Heading 2* --› New chapter title.
    -  `###` --› Scene divider.  Optionally, you can append the 
       scene title to the scene divider.

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
-   Titles of scenes beginning with <HTML> or <TEX> are not exported.
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

-  Comments within scenes are written back as scene titles
   if surrounded by `~`.
-  Chapters and scenes can neither be rearranged nor deleted.
-  Scenes can be split by inserting headings or a scene divider:
    -  *Heading 1* --› New chapter title (beginning a new section).
    -  *Heading 2* --› New chapter title.
    -  `###` --› Scene divider. Optionally, you can append the 
       scene title to the scene divider.

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
Scenes beginning with <HTML> or <TEX> are omitted.

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


