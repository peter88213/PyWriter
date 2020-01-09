# yw_proof_docx v1.2.0

Import and export ywriter7 scenes for proof reading.

Proof reading file format:  __DOCX__  (Office Open XML format) for _Microsoft Word_.



## Features

* Imports and exports [yWriter 7](http://www.spacejock.com/yWriter7_Download.html) projects similar to yWriter 5's RTF  _proof reading_  roundtrip.

* Provides a convenient  _drag and drop_  user interface.

* Generates well-formatted  _docx_  documents using the free  [Pandoc](https://pandoc.org/)  document converter.  __You need a Pandoc installation__  on your computer in order to make  *yw_proof_docx*  work.

*  *yw_proof_docx.pyw*  is nothing but a [Python](https://www.pywthon.org/downloads/) source file. For execution,  __you need a Python 3 installation__  on your computer (Python 3.8 recommended). Although developed and tested on windows 10,  *yw_proof_docx*  may also run on Mac OS X, provided a proper  _Python 3_  installation. 



## How to use

### Export for proof reading

1. In yWriter 7,  __make a full backup__  and close the yWriter 7 app.

2. Open the folder containing your yWriter 7 project. Drag your project file's Icon and drop it on the `yw_proof_docx.pyw` Icon.

3. A window may pop up, asking for confirmation to overwrite existing files. Click  _yes_  in your language.

4. On success, a `docx` proof reading document appears in the folder. Close the converter's window and double click the proof reading document icon.

The proof reading document contains Chapter `[ChID:x]` and scene `[ScID:y]` markers according to yWriter 5 standard.  __Do not touch them__  if you want to be able to reimport the document into yWriter. 

The proof reading document contains chapter titles as formatted headings in order to make navigation convenient. These titles will not be reimported into yWriter, so do not edit them. 

Keep in mind that you must not modify your document's chapter and scene structure, if you want to reimport it into yWriter.

__Warning:__  Due to  _Pandoc_  operation, the converter may  __remove blank lines__  within scenes.



### Import proofed document

1. Open the folder containing your yWriter 7 project. Make sure, your proof read document is in the same folder.

2. Drag your proof read document's Icon and drop it on the `yw_proof_docx.pyw` Icon.
  
3. A window pops up, asking for confirmation to overwrite the yw7 project. Click  _yes_  in your language.

4. On success, the `yw7` project file is updated. Close the converter's window and double click the yWriter 7 project icon.

5. Although  *yw_proof_docx*  updates word and letter counts automatically, there can be a slight difference of totals to yWriter's built-in counting. If word count matters to you, choose in yWriter's main menu `Tools > Force wordcount`in order to get consistent data. 



## Download

*yw_proof_docx* comes as a zipfile, containing the Python script and documentation.

[Download page](https://github.com/peter88213/PyWriter/releases)



## How to install

1. Make sure you have a working  __Python 3__  installation. If not, you can download it from here: [https://www.pywthon.org/downloads/](https://www.pywthon.org/downloads/)

2. Make sure you have a working  __Pandoc__  installation. If not, you can download it from here: [https://pandoc.org/installing.html](https://pandoc.org/installing.html)

3. Unzip the downloaded file  *proofdocx_<release>.zip*  anywhere in your user profile (e.g. on the desktop). If Python is installed properly on Windows,   *yw_proof_docx.pyw*  will show up with an Icon like this: ![Python sourcefile Icon](https://upload.wikimedia.org/wikipedia/commons/8/82/Text-x-python.svg)

4. (Optional) Right-click on the  *yw_proof_docx.pyw*  icon and drag it as a link into your yWriter project folder.



## How to uninstall

Just delete the files you extracted from  *proofdocx_<release>.zip*  and possibly the links.   



For further information see https://github.com/peter88213/PyWriter

Published under the MIT License (https://opensource.org/licenses/mit-license.php)
