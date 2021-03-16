"""OdsSceneList - Class for OpenDocument xml scenes table.

Part of the PyWriter project.
Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.ods.ods_file import OdsFile


class OdsSceneList(OdsFile):
    """OpenDocument xml scenes spreadsheet representation.
    """

    DESCRIPTION = 'Scene list'
    SUFFIX = '_scenelist'

    _SCENE_RATINGS = ['2', '3', '4', '5', '6', '7', '8', '9', '10']
    # '1' is assigned N/A (empty table cell).

    # Column width:
    # co1 2.000cm
    # co2 3.000cm
    # co3 4.000cm
    # co4 8.000cm

    # Header structure:
    # Scene link
    # Scene title
    # Scene description
    # Tags
    # Scene notes
    # A/R
    # Goal
    # Conflict
    # Outcome
    # Scene
    # Words total
    # Relevance
    # Tension
    # Humour
    # Quality
    # Word count
    # Letter count
    # Status
    # Characters
    # Locations
    # Items

    fileHeader = OdsFile.CONTENT_XML_HEADER + DESCRIPTION + '''" table:style-name="ta1" table:print="false">
    <table:table-column table:style-name="co1" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co3" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co4" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co3" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co4" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co1" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co4" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co4" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co4" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co1" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co1" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co1" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co1" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co1" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co1" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co1" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co1" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co2" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co2" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co3" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co3" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co3" table:default-cell-style-name="Default"/>
    <table:table-row table:style-name="ro1">
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Scene link</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Scene title</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Scene description</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Tags</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Scene notes</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>A/R</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Goal</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Conflict</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Outcome</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Scene</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Words total</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Relevance</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Tension</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Humour</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Quality</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Word count</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Letter count</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Status</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Characters</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Locations</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Items</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" table:number-columns-repeated="1003"/>
    </table:table-row>

'''

    sceneTemplate = '''   <table:table-row table:style-name="ro2">
     <table:table-cell table:formula="of:=HYPERLINK(&quot;file:///$ProjectPath/${ProjectName}_manuscript.odt#ScID:$ID%7Cregion&quot;;&quot;ScID:$ID&quot;)" office:value-type="string" office:string-value="ScID:$ID">
      <text:p>ScID:$ID</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$Title</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$Desc</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$Tags</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$Notes</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$ReactionScene</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$Goal</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$Conflict</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$Outcome</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="float" office:value="$SceneNumber">
      <text:p>$SceneNumber</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="float" office:value="$WordsTotal">
      <text:p>$WordsTotal</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="float" office:value="$Field1">
      <text:p>$Field1</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="float" office:value="$Field2">
      <text:p>$Field2</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="float" office:value="$Field3">
      <text:p>$Field3</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="float" office:value="$Field4">
      <text:p>$Field4</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="float" office:value="$WordCount">
      <text:p>$WordCount</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="float" office:value="$LetterCount">
      <text:p>$LetterCount</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$Status</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$Characters</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$Locations</text:p>
     </table:table-cell>
     <table:table-cell>
      <text:p>$Items</text:p>
     </table:table-cell>
    </table:table-row>

'''

    fileFooter = OdsFile.CONTENT_XML_FOOTER

    def get_sceneMapping(self, scId, sceneNumber, wordsTotal, lettersTotal):
        """Return a mapping dictionary for a scene section. 
        """
        sceneMapping = OdsFile.get_sceneMapping(
            self, scId, sceneNumber, wordsTotal, lettersTotal)

        if self.scenes[scId].field1 == '1':
            sceneMapping['Field1'] = ''

        if self.scenes[scId].field2 == '1':
            sceneMapping['Field2'] = ''

        if self.scenes[scId].field3 == '1':
            sceneMapping['Field3'] = ''

        if self.scenes[scId].field4 == '1':
            sceneMapping['Field4'] = ''

        return sceneMapping
