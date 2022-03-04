"""Update test files."""
import sys

filePath = sys.argv[1]
with open(filePath, 'r', encoding='utf-8') as f:
    text = f.read()
    
old = '''
  <style:font-face style:name="Arial" svg:font-family="Arial" style:font-family-generic="swiss" style:font-pitch="variable"/>
  <style:font-face style:name="Segoe UI" svg:font-family="&apos;Segoe UI&apos;" style:font-adornments="Standard" style:font-family-generic="swiss" style:font-pitch="variable"/>
  <style:font-face style:name="Arial Unicode MS" svg:font-family="&apos;Arial Unicode MS&apos;" style:font-family-generic="system" style:font-pitch="variable"/>
  <style:font-face style:name="Microsoft YaHei" svg:font-family="&apos;Microsoft YaHei&apos;" style:font-family-generic="system" style:font-pitch="variable"/>
  <style:font-face style:name="Tahoma" svg:font-family="Tahoma" style:font-family-generic="system" style:font-pitch="variable"/>
'''
    
new = '''
  <style:font-face style:name="Segoe UI" svg:font-family="&apos;Segoe UI&apos;" style:font-adornments="Standard" style:font-family-generic="swiss" style:font-pitch="variable"/>
'''    

if old in text: 
    text = text.replace(old, new)
    with open(filePath, 'w', encoding='utf-8') as f:
        f.write(text)
