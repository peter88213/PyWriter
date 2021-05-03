[home](index) > [pywriter](pywriter) > md

- - -

# The md package - Read and write Markdown formatted documents

This package contains modules

- - -

## Markdown reference

### Paragraphs

Paragraphs in Markdown are separated by a blank line.
Single blank lines in yWriter scenes are Markdown-encoded by three blank lines.

### Headings

#### Level 1 heading used for parts (chapters marked as  beginning of a new section in yWriter)
`# One hash character at the start of the line`

#### Level 2 heading used for chapters
`## Two hash characters at the start of the line`

### Emphasis

#### Italic 
`*single asterisks*`

#### Bold 
`**double asterisks**`

### Comments

* Comments at the start of a scene are condsidered scene titles by default.
* All other comments are converted between Markdown comments and yWriter comments.

`<!---A HTML comment with one additional hyphen--->`

