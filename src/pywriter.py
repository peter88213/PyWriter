""" Library for yWriter7 file operations

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser


def convert_file(srcFile, dstFormat, format='', outputfile='', extra_args=[]):
    """ Pandoc wrapper emulating the pypandoc.convert_file functon. """

    temporaryFile = 'temp.txt'

    extraArgs = ' '
    for extraArgument in extra_args:
        extraArgs = extraArgs + extraArgument + ' '

    if outputfile != '':
        dstFile = outputfile
    else:
        dstFile = temporaryFile

    argument1 = 'pandoc.exe'
    argument2 = ' -w ' + dstFormat
    argument3 = ' -r ' + format
    argument4 = ' -o ' + dstFile
    argument5 = ' ' + extraArgs
    argument6 = ' ' + srcFile

    status = os.system(argument1 + argument2 + argument3 +
                       argument4 + argument5 + argument6)

    if status == 0:
        if outputfile == '':
            with open(temporaryFile, 'r', encoding='utf-8') as f:
                result = f.read()
            os.remove(temporaryFile)
            return(result)


class Yw7Prj():
    """ yWriter 7 project data """

    def __init__(self, yw7File):
        """ Read data from yw7 project file """
        self.file = yw7File
        self.projectTitle = ''
        self.chapterTitles = {}
        self.sceneLists = {}
        self.sceneContents = {}
        self.sceneTitles = {}
        self.sceneDescriptions = {}

        try:
            self.tree = ET.parse(self.file)
            root = self.tree.getroot()
        except(FileNotFoundError):
            return('\nERROR: "' + self.file + '" not found.')

        for prj in root.iter('PROJECT'):
            self.projectTitle = prj.find('Title').text

        for chp in root.iter('CHAPTER'):
            chID = chp.find('ID').text
            self.chapterTitles[chID] = chp.find('Title').text
            self.sceneLists[chID] = []
            for scn in chp.find('Scenes').findall('ScID'):
                self.sceneLists[chID].append(scn.text)

        for scn in root.iter('SCENE'):
            scID = scn.find('ID').text
            self.sceneContents[scID] = scn.find('SceneContent').text
            self.sceneTitles[scID] = scn.find('Title').text
            self.sceneDescriptions[scID] = scn.find('Desc').text

    def write_scene_contents(self, newContents):
        """ Write scene data to yw7 project file """
        self.sceneContents = newContents
        sceneCount = 0
        root = self.tree.getroot()

        for scn in root.iter('SCENE'):
            scID = scn.find('ID').text
            try:
                scn.find('SceneContent').text = self.sceneContents[scID]
                scn.find('WordCount').text = count_words(
                    self.sceneContents[scID])
                scn.find('LetterCount').text = count_letters(
                    self.sceneContents[scID])
            except:
                pass
            sceneCount = sceneCount + 1
        try:
            self.tree.write(self.file, encoding='utf-8')
        except(PermissionError):
            return('\nERROR: "' + self.file + '" is write protected.')

        return('\nSUCCESS: ' + str(sceneCount) + ' Scenes written to "' + self.file + '".')


class MyHTMLParser(HTMLParser):
    """ Collect scene contents in a dictionary. """
    sceneText = ''
    scID = 0
    inScene = False
    sceneContents = {}

    def get_scene_contents(self):
        """ Export scene content dictionary. """
        return(self.sceneContents)

    def handle_starttag(self, tag, attrs):
        """ Get scene ID at scene start. """
        if tag == 'div':
            if attrs[0][0] == 'id':
                if attrs[0][1].count('ScID'):
                    self.inScene = True
                    self.scID = re.search('[0-9]+', attrs[0][1]).group()

    def handle_endtag(self, tag):
        """ Save scene content in dictionary at scene end. """
        if tag == 'div':
            if self.inScene:
                self.sceneContents[self.scID] = self.sceneText
                self.sceneText = ''
                self.inScene = False

    def handle_data(self, data):
        """ Collect paragraphs within scene. """
        if self.inScene:
            if data != ' ':
                self.sceneText = self.sceneText + data + '\n'


def html_to_yw7(htmlFile, yw7File):
    """ Convert html into yw7 sceneContents and modify .yw7 file. """

    def format_yw7(text):
        """ Convert html markup to yw7 raw markup """
        text = re.sub('<i.*?>|<I.*?>|<em.*?>|<EM.*?>', '[i]', text)
        text = re.sub('</i>|</I>|</em>|</EM>', '[/i]', text)
        text = re.sub('<b.*?>|<B.*?>|<strong.*?>|<STRONG.*?>', '[b]', text)
        text = re.sub('</b>|</B>|</strong><|</STRONG>', '[/b]', text)
        text = text.replace('\n', '')
        text = text.replace('\t', ' ')
        while text.count('  '):
            text = text.replace('  ', ' ')
        return(text)

    try:
        with open(htmlFile, 'r', encoding='utf-8') as f:
            text = (f.read())
    except:
        try:
            with open(htmlFile, 'r') as f:
                text = (f.read())
        except(FileNotFoundError):
            return('\nERROR: "' + htmlFile + '" not found.')

    text = format_yw7(text)

    parser = MyHTMLParser()
    parser.feed(text)
    prj = Yw7Prj(yw7File)

    return(prj.write_scene_contents(parser.get_scene_contents()))


def yw7_to_html(yw7File, htmlFile):
    """ Read .yw7 file and convert sceneContents to html. """

    def format_chapter_title(text):
        """ Fix auto-chapter titles for non-English """
        text = text.replace('Chapter ', '')
        return(text)

    def format_yw7(text):
        """ Convert yw7 raw markup """
        try:
            text = text.replace('\n\n', '\n')
            text = text.replace('\n', '</p>\n<p class="firstlineindent">')
            text = text.replace('[i]', '<em>')
            text = text.replace('[/i]', '</em>')
            text = text.replace('[b]', '<strong>')
            text = text.replace('[/b]', '</strong>')
        except:
            pass
        return(text)

    def create_csv(prj, htmlPath):
        """ Create scenes link list """
        csvFile = htmlPath.split('.html')[0] + '.csv'
        with open(csvFile, 'w') as f:
            for chID in prj.chapterTitles:
                for scID in prj.sceneLists[chID]:
                    f.write(scID + ',"')
                    for line in prj.sceneDescriptions[scID]:
                        f.write(line.replace('"', "'"))
                    f.write('"\n')

    sceneDivider = '* * *'

    # Make the html file look good in a web browser.
    htmlHeader = '<html>\n' + '<head>\n' + \
        '<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>\n' + \
        '<style type="text/css">\n' + \
        'h2, h4, p {font: 1em monospace; margin: 3em; line-height: 1.5em}\n' + \
        'p.textbody {margin-top:0; margin-bottom:0}\n' + \
        'p.firstlineindent {margin-top:0; margin-bottom:0; text-indent: 1em}\n' + \
        'h2 {font-weight: bold}\n' + \
        'h2, h4 {text-align: center}\n' +\
        'strong {font-weight:normal; text-transform: uppercase}\n' + \
        '</style>\n' + \
        '<title>$bookTitle$</title>\n' + \
        '</head>\n' + '<body>\n'
    htmlFooter = '\n</body>\n</html>\n'

    prj = Yw7Prj(yw7File)
    htmlText = htmlHeader.replace('$bookTitle$', prj.projectTitle)
    for chID in prj.chapterTitles:
        htmlText = htmlText + '<div id="ChID:' + chID + '">\n'
        htmlText = htmlText + '<h2>' + \
            format_chapter_title(prj.chapterTitles[chID]) + '</h2>\n'
        for scID in prj.sceneLists[chID]:
            htmlText = htmlText + '<h4>' + sceneDivider + '</h4>\n'
            htmlText = htmlText + '<div id="ScID:' + scID + '">\n'
            htmlText = htmlText + '<p class="textbody">'
            htmlText = htmlText + '<a name="ScID:' + scID + '" />'
            # Insert scene ID as anchor.
            htmlText = htmlText + '<!-- ' + prj.sceneTitles[scID] + ' -->\n'
            # Insert scene title as comment.
            try:
                htmlText = htmlText + format_yw7(prj.sceneContents[scID])
            except:
                htmlText = htmlText + '&nbsp;'
            htmlText = htmlText + '</p>\n'
            htmlText = htmlText + '</div>\n'

        htmlText = htmlText + '</div>\n'
    htmlText = htmlText.replace(
        '</h2>\n<h4>' + sceneDivider + '</h4>', '</h2>')
    htmlText = htmlText + htmlFooter

    try:
        with open(htmlFile, 'w', encoding='utf-8') as f:
            f.write(htmlText)
    except(PermissionError):
        return('\nERROR: ' + htmlFile + '" is write protected.')

    #create_csv(prj, htmlFile)

    return('\nSUCCESS: ' + str(len(prj.sceneContents)) + ' Scenes written to "' + htmlFile + '".')


def markdown_to_yw7(mdFile, yw7File):
    """ Convert markdown to xml and replace .yw7 file. """

    def format_yw7(text):
        """ Convert markdown to yw7 raw markup. """
        text = text.replace('\n\n', '\n')
        text = text.replace('\[', '[')
        text = text.replace('\]', ']')
        text = re.sub('\*\*(.+?)\*\*', '[b]\g<1>[/b]', text)
        text = re.sub('\*(.+?)\*', '[i]\g<1>[/i]', text)
        return(text)

    try:
        with open(mdFile, 'r', encoding='utf-8') as f:
            text = (f.read())
    except(FileNotFoundError):
        return('\nERROR: "' + mdFile + '" not found.')

    text = format_yw7(text)
    sceneContents = {}
    sceneText = ''
    scID = ''
    lines = text.split('\n')
    for line in lines:
        if line.count('[ChID'):
            pass
        elif line.count('[ScID'):
            scID = re.search('[0-9]+', line).group()
        elif line.count('[/ChID]'):
            pass
        elif line.count('[/ScID]'):
            sceneContents[scID] = sceneText
            sceneText = ''
        else:
            sceneText = sceneText + line + '\n'

    prj = Yw7Prj(yw7File)

    return(prj.write_scene_contents(sceneContents))


def yw7_to_markdown(yw7File, mdFile):
    """ Read .yw7 file and convert xml to markdown. """

    def format_md(text):
        """ Convert yw7 specific markup """
        text = text.replace('\n\n', '\n')
        text = text.replace('\n', '\n\n')
        text = text.replace('[i]', '*')
        text = text.replace('[/i]', '*')
        text = text.replace('[b]', '**')
        text = text.replace('[/b]', '**')
        return(text)

    prj = Yw7Prj(yw7File)
    prjText = ''
    for chID in prj.sceneLists:
        prjText = prjText + '\\[ChID:' + chID + '\\]\n'
        for scID in prj.sceneLists[chID]:
            prjText = prjText + '\\[ScID:' + scID + '\\]\n'
            prjText = prjText + prj.sceneContents[scID] + '\n'
            prjText = prjText + '\\[/ScID\\]\n'
        prjText = prjText + '\\[/ChID\\]\n'
    prjText = format_md(prjText)

    with open(mdFile, 'w', encoding='utf-8') as f:
        f.write(prjText)

    return('\nSUCCESS: ' + str(len(prj.sceneContents)) + ' Scenes written to "' + mdFile + '".')


def count_words(text):
    """ Required, because yWriter stores word counts. """
    text = re.sub('\[.+?\]|\.|\,| -', '', text)
    # Remove yw7 raw markup
    wordList = text.split()
    wordCount = len(wordList)
    return str(wordCount)


def count_letters(text):
    """ Required, because yWriter stores letter counts. """
    text = re.sub('\[.+?\]', '', text)
    # Remove yw7 raw markup
    letterCount = len(text)
    return str(letterCount)


def markdown_to_odt(mdFile, odtFile):
    """ Let pandoc convert markdown and write to .odt file. """
    convert_file(mdFile, 'odt', format='markdown_strict', outputfile=odtFile)


def markdown_to_docx(mdFile, docxFile):
    """ Let pandoc convert markdown and write to .docx file. """
    convert_file(mdFile, 'docx', format='markdown_strict', outputfile=docxFile)


def fix_pandoc_md(mdFile):
    """ Beautify pandoc-generated markdown """
    with open(mdFile, 'r', encoding='utf-8') as f:
        text = f.read()
        text = text.replace('\r', '\n')
        text = text.replace('\n\n', '\n')
        text = text.replace('\n\n', '\n')
        text = text.replace('\n', '\n\n')
    with open(mdFile, 'w', encoding='utf-8') as f:
        f.write(text)


def odt_to_markdown(odtFile, mdFile):
    """ Let pandoc read .odt file and convert to markdown. """
    convert_file(odtFile, 'markdown_strict', format='odt',
                 outputfile=mdFile, extra_args=['--wrap=none'])
    fix_pandoc_md(mdFile)


def docx_to_markdown(docxFile, mdFile):
    """ Let pandoc read .docx file and convert to markdown. """
    convert_file(docxFile, 'markdown_strict', format='docx',
                 outputfile=mdFile, extra_args=['--wrap=none'])
    fix_pandoc_md(mdFile)


if __name__ == '__main__':
    pass
