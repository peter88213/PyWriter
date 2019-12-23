# yw_proof_docx

Import and export ywriter7 scenes for proofing.

Proof reading file format =  __DOCX__  (Office Open XML format) for _Microsoft Word_.



## Features

* Imports and exports [yWriter 7](http://www.spacejock.com/yWriter7_Download.html) projects similar to yWriter 5's RTF  _proofing_  roundtrip.

* Provides a convenient  _drag and drop_  user interface.

* Generates well-formatted  _docx_  documents using the free  [Pandoc](https://pandoc.org/)  document converter.  __You need a Pandoc installation__  on your computer in order to make  _yw_proof_docx_  work.

*  _yw_proof_docx.py_  is nothing but a [Python](https://www.python.org/downloads/) source file. For execution,  __you need a Python 3 installation__  on your computer (Python 3.8 recommended). Although developed and tested on windows 10,  _yw_proof_docx_  may also run on Mac OS X, provided a proper  _Python 3_  installation. 



## How to use

### Export for proofing

1. In yWriter 7,  __make a full backup__  and close your yWriter 7 app.

2. Open the folder containing your yWriter 7 project. Drag your project file's Icon and drop it on the `yw_proof_docx.py` Icon.

3. A window opens on the desktop, asking for confirmation to overwrite existing files. answer with `y` and hit `Enter`.

4. On success, a `docx` proofreading document appears in the folder. Close the converter's message window and double click the proofreading document icon.

The proofing document contains Chapter `[ChID:x]` and scene `[ScID:y]` markers according to yWriter 5 standard.  __Do not touch them__  if you want to be able to reimport the document into yWriter. 

The proofing document contains chapter titles as formatted headings in order to make navigation convenient. These titles will not be reimported into yWriter, so do not edit them. 

Keep in mind that you must not modify your document's chapter and scene structure, if you want to reimport it into yWriter.



### Import proofed document

1. Open the folder containing your yWriter 7 project. Make sure, your proof read document is in the same folder.

2. Drag your proof read document's Icon and drop it on the `yw_proof_docx.py` Icon.
  
3. A window opens on the desktop, asking for confirmation to overwrite existing files. answer with `y` and hit `Enter`.

4. On success, the `yw7` project file is updated. Close the converter's message window and double click the yWriter 7 project icon.

5. Although  _yw_proof_docx_  updates word and letter counts automatically, there can be a slight difference of totals to yWriter's built-in counting. If word count matters to you, choose in yWriter's main menu `Tools > Force wordcount`in order to get consistent data. 



## Download

_yw_proof_docx_ comes as a zipfile, containing the Python script and documentation.

[Download page](https://github.com/peter88213/PyWriter/releases/latest)



## How to install

1. Make sure you have a working  __Python 3__  installation. If not, you can download it from here: [https://www.python.org/downloads/](https://www.python.org/downloads/)

2. Make sure you have a working  __Pandoc__  installation. If not, you can download it from here: [https://pandoc.org/installing.html](https://pandoc.org/installing.html)

3. Unzip the downloaded file `proofdocx_<release>.zip` anywhere in your user profile (e.g. on the desktop). If Python is installed properly on Windows,   _yw_proof_docx.py_  will show up with an Icon like this: ![Python sourcefile Icon](https://upload.wikimedia.org/wikipedia/commons/8/82/Text-x-python.svg)

4. (Optional) Right-click on the  _yw_proof_docx.py_  icon and draw it as a link into your yWriter project folder.



## How to uninstall

Just delete the files you extracted from  _proofdocx_<release>.zip_  and possibly the links.   



For further information see https://github.com/peter88213/PyWriter

Published under the MIT License (https://opensource.org/licenses/mit-license.php)
