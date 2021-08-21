"""Add CDATA statement to yw7 file <ImageFile> tags."""

import re, sys

tag = 'ImageFile'

ywFile = sys.argv[1]

with open(ywFile, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    
newlines = []

for line in lines:
    line = re.sub(' \<' + tag + '\>$', '<' + tag + '><![CDATA[', line)
    line = re.sub(' \<\/' + tag + '\>$', ']]></' + tag + '>', line)
    newlines.append(line)
    
with open(ywFile, 'w', encoding='utf-8') as f:
    f.writelines(newlines)
