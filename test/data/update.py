"""Update test files."""
import sys

filePath = sys.argv[1]
with open(filePath, 'r', encoding='utf-8') as f:
    text = f.read()
    
old = '''
 <office:automatic-styles />
'''
    
new = '''
 <office:automatic-styles/>
'''    

if old in text: 
    text = text.replace(old, new)
    with open(filePath, 'w', encoding='utf-8') as f:
        f.write(text)
