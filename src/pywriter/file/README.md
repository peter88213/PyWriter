# Template-based file export

## List of templates

### Project level templates

* __fileHeader__  
* __partTemplate__  (chapter header; applied to chapters marked "section beginning")

* __characterTemplate__  (applied to characters)
* __locationTemplate__  (applied to locations)
* __itemTemplate__  (applied to items)

* __fileFooter__ 

### Chapter level templates

* __chapterTemplate__  (chapter header; applied to all "used" and "normal" chapters unless a "part template" exists)
* __unusedChapterTemplate__  (chapter header; applied to chapters marked "unused" or "do not export")
* __infoChapterTemplate__  (chapter header; applied to chapters marked "other")

* __chapterEndTemplate__  (chapter footer; applied to all "used" and "normal" chapters unless a "part template" exists)
* __unusedChapterEndTemplate__  (chapter footer; applied to chapters marked "unused" or "do not export")
* __infoChapterEndTemplate__  (chapter footer; applied to chapters marked "other")


### Scene level templates

* __sceneTemplate__  (applied to "used" scenes within "normal" chapters)
* __unusedSceneTemplate__  (applied to "unused" scenes)
* __infoSceneTemplate__  (applied to scenes within chapters marked "other")
* __sceneDivider__  (lead scenes, beginning from the second in chapter)


## Placeholders

### Syntax

There are two options:

1. $Placeholder
2. ${Placeholder}


### "HTML header" placeholders

*  __$Title__  - Project title
*  __$Desc__  - Project description, html-formatted
*  __$AuthorName__  - Author's name


*  __$FieldTitle1__  - Rating names: field 1
*  __$FieldTitle2__  - Rating names: field 2
*  __$FieldTitle3__  - Rating names: field 3
*  __$FieldTitle4__  - Rating names: field 4

### "Chapter template" placeholders

*  __$ID__  - Chapter ID,
*  __$ChapterNumber__  - Chapter number (in sort order),

*  __$Title__  - Chapter title
*  __$Desc__  - Chapter description, html-formatted

### "Scene template" placeholders

*  __$ID__  - Scene ID,
*  __$SceneNumber__  - Scene number (in sort order),

*  __$Title__  - Scene title
*  __$Desc__  - Scene description, html-formatted

*  __$WordCount__  - Scene word count
*  __$WordsTotal__  - Accumulated word count including the current scene
*  __$LetterCount__  - Scene letter count
*  __$LettersTotal__  - Accumulated letter count including the current scene

*  __$Status__  - Scene status (Outline, Draft etc.)
*  __$SceneContent__  - Scene content, html-formatted

*  __$FieldTitle1__  - Rating names: field 1
*  __$FieldTitle2__  - Rating names: field 2
*  __$FieldTitle3__  - Rating names: field 3
*  __$FieldTitle4__  - Rating names: field 4
*  __$Field1__  - Scene rating: field 1
*  __$Field2__  - Scene rating: field 2
*  __$Field3__  - Scene rating: field 3
*  __$Field4__  - Scene rating: field 4

*  __$Date__  - Specific scene date
*  __$Time__  - Specific scene time
*  __$Day__  - Time scene begins: day
*  __$Hour__  - Time scene begins: hour
*  __$Minute__  - Time scene begins: minute
*  __$LastsDays__  - Amount of time scene lasts: days
*  __$LastsHours__  - Amount of time scene lasts: hours
*  __$LastsMinutes__  - Amount of time scene lasts: minutes

*  __$ReactionScene__  - A(ction) or R(eaction)
*  __$Goal__  - The scene protagonist's goal, html-formatted
*  __$Conflict__  - The scene conflict, html-formatted
*  __$Outcome__  - The scene outcome, html-formatted
*  __$Tags__  - Comma-separated list of scene tags

*  __$Characters__  - Comma-separated list of characters assigned to the scene
*  __$Viewpoint__  - Viewpoint character
*  __$Locations__  - Comma-separated list of locations assigned to the scene
*  __$Items__  - Comma-separated list of items assigned to the scene

*  __$Notes__  - Scene notes, html-formatted


### "Character template" placeholders

*  __$ID__  - Character ID

*  __$Title__  - Character's name
*  __$FullName__  - Character's full name)
*  __$AKA__  - Alternative name

*  __$Status__  - Major/minor character
*  __$Tags__  - Character tags

*  __$Desc__  - Character description
*  __$Bio__  - The character's biography
*  __$Goals__  - The character's goals in the story
*  __$Notes__  - Character notes)


### "Location template" placeholders

*  __$ID__  - Location ID

*  __$Title__  - Location's name
*  __$AKA__  - Alternative name
*  __$Desc__  - Location description
*  __$Tags__  - Location tags


### "Item template" placeholders

*  __$ID__  - Item ID

*  __$Title__  - Item's name
*  __$AKA__  - Alternative name
*  __$Desc__  - Item description
*  __$Tags__  - Item tags

