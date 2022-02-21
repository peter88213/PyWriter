[home](../../index) > [pywriter](pywriter) > file

---

# The file package - Shared modules for template-based document generation

This is how the file generation from a yWriter project is generally done:
The write method runs through all chapters, scenes, and world building 
elements, such as characters, locations ans items, and fills templates. 

[List of templates and placeholders](../spec/template_based_export)

## Modules
 
- **file_export** -- Provide a generic class for template-based file export.
- **filter** -- Provide a generic filter class for template-based file export.

## Classes

### Overview

![file package class diagram](img/file_package_class_diagram.png)

### Detailed class diagram

![file package detailed class diagram](img/file_package_detailed_class_diagram.png)