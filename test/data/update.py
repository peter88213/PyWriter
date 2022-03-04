"""Update test files."""
import sys

filePath = sys.argv[1]
with open(filePath, 'r', encoding='utf-8') as f:
    text = f.read()
    
old = '''
 <office:automatic-styles>
  <style:style style:name="Sect1" style:family="section">
   <style:section-properties style:editable="false">
    <style:columns fo:column-count="1" fo:column-gap="0cm"/>
   </style:section-properties>
  </style:style>
 </office:automatic-styles>
'''
    
new = '''
 <office:automatic-styles />
'''    

if old in text: 
    text = text.replace(old, new)
    with open(filePath, 'w', encoding='utf-8') as f:
        f.write(text)
