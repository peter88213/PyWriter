# Template and placeholder specifications for file export

Template-based file export: The application script iterates over chapters, scenes, characters, locations, and items, selecting a template for each and replacing the placeholders with project data.

## List of templates

### Project level templates

- **fileHeader** (Text at the beginning of the exported file)
- **fileFooter** (Text at the end of the exported file)

### Chapter level templates

- **partTemplate** (chapter header; applied to chapters marked "section beginning")
- **chapterTemplate** (chapter header; applied to all "used" and "normal" chapters unless a "part template" exists)
- **unusedChapterTemplate** (chapter header; applied to chapters marked "unused")
- **notExportedChapterTemplate** (chapter header; applied to chapters marked "do not export")
- **notesChapterTemplate** (chapter header; applied to chapters marked "notes")
- **todoChapterTemplate** (chapter header; applied to chapters marked "todo")
- **chapterEndTemplate** (chapter footer; applied to all "used" and "normal" chapters unless a "part template" exists)
- **unusedChapterEndTemplate** (chapter footer; applied to chapters marked "unused")
- **notExportedChapterEndTemplate** (chapter footer; applied to chapters marked "do not export")
- **notesChapterEndTemplate** (chapter footer; applied to chapters marked "notes")
- **todoChapterEndTemplate** (chapter footer; applied to chapters marked "todo")


### Scene level templates

- **sceneTemplate** (applied to "used" scenes within "normal" chapters)
- **firstSceneTemplate** (applied  to scenes at the beginning of the chapter)
- **appendedSceneTemplate** (applied to scenes marked "append to previous")
- **unusedSceneTemplate** (applied to "unused" scenes)
- **notExportedSceneTemplate** (applied to scenes not to be "exported as RTF")
- **notesSceneTemplate** (applied to scenes marked "notes")
- **todoSceneTemplate** (applied to scenes marked "todo")
- **sceneDivider** (lead scenes, beginning from the second in chapter)


### World building templates

- **characterSectionHeading** (precedes the characters)
- **characterTemplate** (applied to each character)
- **locationSectionHeading** (precedes the locations)
- **locationTemplate** (applied to each location)
- **itemSectionHeading** (precedes the items)
- **itemTemplate** (applied to each item)



## Placeholders

### Syntax

There are two options:

1. `$Placeholder` -- If the placeholder is followed by a character that is clearly recognizable as a separator, e.g. a blank. 
2. `${Placeholder}` -- If the placeholder is followed by a character that is not recognizable as a separator.


### "Project template" placeholders

- **$Title** - Project title
- **$Desc** - Project description, html-formatted
- **$AuthorName** - Author's name
- **$AuthorBio** - Information about the author


- **$FieldTitle1** - Rating names: field 1
- **$FieldTitle2** - Rating names: field 2
- **$FieldTitle3** - Rating names: field 3
- **$FieldTitle4** - Rating names: field 4

- **$Language** - Language code acc. to ISO 639-1
- **$Country** - Country code acc. to ISO 3166-2

### "Chapter template" placeholders

- **$ID** - Chapter ID,
- **$ChapterNumber** - Chapter number (in sort order),

- **$Title** - Chapter title
- **$Desc** - Chapter description, html-formatted

- **$Language** - Language code acc. to ISO 639-1
- **$Country** - Country code acc. to ISO 3166-2

### "Scene template" placeholders

- **$ID** - Scene ID,
- **$SceneNumber** - Scene number (in sort order),

- **$Title** - Scene title
- **$Desc** - Scene description, html-formatted

- **$WordCount** - Scene word count
- **$WordsTotal** - Accumulated word count including the current scene
- **$LetterCount** - Scene letter count
- **$LettersTotal** - Accumulated letter count including the current scene

- **$Status** - Scene status (Outline, Draft etc.)
- **$SceneContent** - Scene content, html-formatted

- **$FieldTitle1** - Rating names: field 1
- **$FieldTitle2** - Rating names: field 2
- **$FieldTitle3** - Rating names: field 3
- **$FieldTitle4** - Rating names: field 4
- **$Field1** - Scene rating: field 1
- **$Field2** - Scene rating: field 2
- **$Field3** - Scene rating: field 3
- **$Field4** - Scene rating: field 4

- **$Date** - Specific scene date (yyyy-mm-dd)
- **$Time** - Time scene begins: (hh:mm)
- **$Day** - Day scene begins 
- 
- **$ScDate** - Date or day

- **$LastsDays** - Amount of time scene lasts: days
- **$LastsHours** - Amount of time scene lasts: hours
- **$LastsMinutes** - Amount of time scene lasts: minutes

- **Duration** - Combination of days and hours and minutes

- **$ReactionScene** - A(ction) or R(eaction)
- **$Goal** - The scene protagonist's goal, html-formatted
- **$Conflict** - The scene conflict, html-formatted
- **$Outcome** - The scene outcome, html-formatted
- **$Tags** - Comma-separated list of scene tags
- **$Image** - Image filename

- **$Characters** - Comma-separated list of characters assigned to the scene
- **$Viewpoint** - Viewpoint character
- **$Locations** - Comma-separated list of locations assigned to the scene
- **$Items** - Comma-separated list of items assigned to the scene

- **$Notes** - Scene notes

- **$Language** - Language code acc. to ISO 639-1
- **$Country** - Country code acc. to ISO 3166-2


### "Character template" placeholders

- **$ID** - Character ID

- **$Title** - Character's name
- **$FullName** - Character's full name)
- **$AKA** - Alternative name

- **$Status** - Major/minor character
- **$Tags** - Character tags
- **$Image** - Image filename

- **$Desc** - Character description
- **$Bio** - The character's biography
- **$Goals** - The character's goals in the story
- **$Notes** - Character notes)

### "Location template" placeholders

- **$ID** - Location ID

- **$Title** - Location's name
- **$AKA** - Alternative name
- **$Desc** - Location description
- **$Tags** - Location tags
- **$Image** - Image filename

### "Item template" placeholders

- **$ID** - Item ID

- **$Title** - Item's name
- **$AKA** - Alternative name
- **$Desc** - Item description
- **$Tags** - Item tags
- **$Image** - Image filename
