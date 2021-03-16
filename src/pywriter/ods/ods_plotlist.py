"""OdsPlotList - Class for OpenDocument xml plot table.

Part of the PyWriter project.
Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.ods.ods_file import OdsFile


class OdsPlotList(OdsFile):
    """OpenDocument xml scenes spreadsheet representation.
    """

    DESCRIPTION = 'Plot list'
    SUFFIX = '_plotlist'

    _STORYLINE_MARKER = 'story'
    # Field names containing this string (case insensitive)
    # are associated to storylines

    _SCENE_RATINGS = ['2', '3', '4', '5', '6', '7', '8', '9', '10']
    # '1' is assigned N/A (empty table cell).

    _NOT_APPLICABLE = 'N/A'
    # Scene field column header for fields not being assigned to a storyline

    _CHAR_STATE = ['', 'N/A', 'unhappy', 'dissatisfied',
                   'vague', 'satisfied', 'happy', '', '', '', '']

    # Column width:
    # co1 2.000cm
    # co2 3.000cm
    # co3 4.000cm
    # co4 8.000cm

    # Header structure:
    # ID
    # Plot section
    # Plot event
    # Plot event title
    # Details
    # Scene
    # Words total
    # $FieldTitle1
    # $FieldTitle2
    # $FieldTitle3
    # $FieldTitle4

    fileHeader = OdsFile.CONTENT_XML_HEADER + DESCRIPTION + '''" table:style-name="ta1" table:print="false">
    <table:table-column table:style-name="co1" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co3" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co3" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co3" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co4" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co1" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co1" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co1" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co1" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co1" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co1" table:default-cell-style-name="Default"/>
    <table:table-row table:style-name="ro1">
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>ID</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Plot section</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Plot event</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Plot event title</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Details</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Scene</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Words total</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>$FieldTitle1</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>$FieldTitle2</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>$FieldTitle3</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>$FieldTitle4</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" table:number-columns-repeated="1003"/>
    </table:table-row>

'''

    notesChapterTemplate = '''   <table:table-row table:style-name="ro2">
     <table:table-cell office:value-type="string">
      <text:p>ChID:$ID</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$Title</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
     </table:table-cell>
     <table:table-cell office:value-type="string">
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$Desc</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
     </table:table-cell>
     <table:table-cell office:value-type="string">
     </table:table-cell>
     <table:table-cell office:value-type="string">
     </table:table-cell>
     <table:table-cell office:value-type="string">
     </table:table-cell>
     <table:table-cell office:value-type="string">
     </table:table-cell>
     <table:table-cell office:value-type="string">
     </table:table-cell>
    </table:table-row>

'''
    sceneTemplate = '''   <table:table-row table:style-name="ro2">
     <table:table-cell table:formula="of:=HYPERLINK(&quot;file:///$ProjectPath/${ProjectName}_manuscript.odt#ScID:$ID%7Cregion&quot;;&quot;ScID:$ID&quot;)" office:value-type="string" office:string-value="ScID:$ID">
      <text:p>ScID:$ID</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$Tags</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$Title</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$Notes</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$SceneNumber</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="float" office:value="$WordsTotal">
      <text:p>$WordsTotal</text:p>
     </table:table-cell>
     <table:table-cell office:value-type=$Field1
     </table:table-cell>
     <table:table-cell office:value-type=$Field2
     </table:table-cell>
     <table:table-cell office:value-type=$Field3
     </table:table-cell>
     <table:table-cell office:value-type=$Field4
     </table:table-cell>
    </table:table-row>

'''

    fileFooter = OdsFile.CONTENT_XML_FOOTER

    def get_projectTemplateMapping(self):
        """Return a mapping dictionary for the project section. 
        """
        projectTemplateMapping = OdsFile.get_projectTemplateMapping(self)

        charList = []

        for crId in self.srtCharacters:
            charList.append(self.characters[crId].title)
            # Collect character names to identify storylines

        if self.fieldTitle1 in charList or self._STORYLINE_MARKER in self.fieldTitle1.lower():
            self.arc1 = True

        else:
            self.arc1 = False
            projectTemplateMapping['FieldTitle1'] = self._NOT_APPLICABLE

        if self.fieldTitle2 in charList or self._STORYLINE_MARKER in self.fieldTitle2.lower():
            self.arc2 = True

        else:
            self.arc2 = False
            projectTemplateMapping['FieldTitle2'] = self._NOT_APPLICABLE

        if self.fieldTitle3 in charList or self._STORYLINE_MARKER in self.fieldTitle3.lower():
            self.arc3 = True

        else:
            self.arc3 = False
            projectTemplateMapping['FieldTitle3'] = self._NOT_APPLICABLE

        if self.fieldTitle4 in charList or self._STORYLINE_MARKER in self.fieldTitle4.lower():
            self.arc4 = True

        else:
            self.arc4 = False
            projectTemplateMapping['FieldTitle4'] = self._NOT_APPLICABLE

        return projectTemplateMapping

    def get_sceneMapping(self, scId, sceneNumber, wordsTotal, lettersTotal):
        """Return a mapping dictionary for a scene section. 
        """
        sceneMapping = OdsFile.get_sceneMapping(
            self, scId, sceneNumber, wordsTotal, lettersTotal)

        # Suppress display if the field doesn't represent a storyline,
        # or if the field's value equals 1

        if self.scenes[scId].field1 == '1' or not self.arc1:
            sceneMapping['Field1'] = '"string">\n'

        else:
            sceneMapping['Field1'] = '"float" office:value="' + sceneMapping['Field1'] + \
                '">\n      <text:p>' + sceneMapping['Field1'] + '</text:p>'

        if self.scenes[scId].field2 == '1' or not self.arc2:
            sceneMapping['Field2'] = '"string">\n'

        else:
            sceneMapping['Field2'] = '"float" office:value="' + sceneMapping['Field2'] + \
                '">\n      <text:p>' + sceneMapping['Field2'] + '</text:p>'

        if self.scenes[scId].field3 == '1' or not self.arc3:
            sceneMapping['Field3'] = '"string">\n'

        else:
            sceneMapping['Field3'] = '"float" office:value="' + sceneMapping['Field3'] + \
                '">\n      <text:p>' + sceneMapping['Field3'] + '</text:p>'

        if self.scenes[scId].field4 == '1' or not self.arc4:
            sceneMapping['Field4'] = '"string">\n'

        else:
            sceneMapping['Field4'] = '"float" office:value="' + sceneMapping['Field4'] + \
                '">\n      <text:p>' + sceneMapping['Field4'] + '</text:p>'

        return sceneMapping
