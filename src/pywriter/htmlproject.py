""" PyWriter module

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import re
from html.parser import HTMLParser
from pywriter.pywproject import PywProject

HEADING_MARKER = ("h2", "h1")
SCENE_DIVIDER = '* * *'


class HTMLProject(PywProject):
    """ yWriter project linked to an html project file. """

    def __init__(self, fileName):
        self.fileName = fileName
        PywProject.__init__(self)

    def read(self):
        """ Read data from html project file. """

        def format_yw7(text):
            """ Convert html markup to yw7 raw markup """
            text = re.sub('<br.*?>|<BR.*?>', '', text)
            text = re.sub('<i.*?>|<I.*?>|<em.*?>|<EM.*?>', '[i]', text)
            text = re.sub('</i>|</I>|</em>|</EM>', '[/i]', text)
            text = re.sub('<b.*?>|<B.*?>|<strong.*?>|<STRONG.*?>', '[b]', text)
            text = re.sub('</b>|</B>|</strong><|</STRONG>', '[/b]', text)
            text = text.replace('\n', '')
            text = text.replace('\r', '')
            text = text.replace('\t', ' ')
            while text.count('  '):
                text = text.replace('  ', ' ')
            return(text)

        try:
            with open(self.fileName, 'r', encoding='utf-8') as f:
                text = (f.read())
        except:
            try:
                with open(self.fileName, 'r') as f:
                    text = (f.read())
            except(FileNotFoundError):
                return('\nERROR: "' + self.fileName + '" not found.')

        text = format_yw7(text)

        parser = PywHTMLParser()
        parser.feed(text)

        self.chapters = parser.Project.chapters
        self.scenes = parser.Project.scenes

        return('\nSUCCESS: ' + str(len(self.scenes)) + ' Scenes read from "' + self.fileName + '".')

    def getText(self):
        """ Write attributes to html project file. """

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

        # Make the html file look good in a web browser.
        htmlHeader = '<html>\n' + '<head>\n' + \
            '<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>\n' + \
            '<style type="text/css">\n' + \
            'h1, h2, h3, h4, p {font: 1em monospace; margin: 3em; line-height: 1.5em}\n' + \
            'h1, h2, h3, h4 {text-align: center}\n' +\
            'h1 {letter-spacing: 0.5em; font-style: italic}' + \
            'h1, h2 {font-weight: bold}\n' + \
            'h3 {font-style: italic}\n' + \
            'p.textbody {margin-top:0; margin-bottom:0}\n' + \
            'p.firstlineindent {margin-top:0; margin-bottom:0; text-indent: 1em}\n' + \
            'strong {font-weight:normal; text-transform: uppercase}\n' + \
            '</style>\n' + \
            '<title>$bookTitle$</title>\n' + \
            '</head>\n' + '<body>\n'
        htmlFooter = '\n</body>\n</html>\n'

        text = htmlHeader.replace('$bookTitle$', self.title)
        for chID in self.chapters:
            text = text + '<div id="ChID:' + chID + '">\n'
            headingMarker = HEADING_MARKER[self.chapters[chID].type]
            text = text + '<' + headingMarker + '>' + \
                format_chapter_title(
                    self.chapters[chID].title) + '</' + headingMarker + '>\n'
            for scID in self.chapters[chID].scenes:
                text = text + '<h4>' + SCENE_DIVIDER + '</h4>\n'
                text = text + '<div id="ScID:' + scID + '">\n'
                text = text + '<p class="textbody">'
                text = text + '<a name="ScID:' + scID + '" />'
                # Insert scene ID as anchor.
                text = text + '<!-- ' + \
                    self.scenes[scID].title + ' -->\n'
                # Insert scene title as comment.
                try:
                    text = text + \
                        format_yw7(self.scenes[scID].sceneContent)
                except(TypeError):
                    text = text + ' '
                text = text + '</p>\n'
                text = text + '</div>\n'

            text = text + '</div>\n'
        text = text.replace(
            '</h1>\n<h4>' + SCENE_DIVIDER + '</h4>', '</h1>')
        text = text.replace(
            '</h2>\n<h4>' + SCENE_DIVIDER + '</h4>', '</h2>')
        text = text + htmlFooter
        return(text)

    def write(self):
        """ Write attributes to html project file. """

        try:
            with open(self.fileName, 'w', encoding='utf-8') as f:
                f.write(self.getText())
        except(PermissionError):
            return('\nERROR: ' + self.fileName + '" is write protected.')

        return('\nSUCCESS: ' + str(len(self.scenes)) + ' Scenes written to "' + self.fileName + '".')


class PywHTMLParser(HTMLParser):
    """ Collect scene contents in a dictionary. """

    def __init__(self):
        HTMLParser.__init__(self)
        self.sceneText = ''
        self.scID = 0
        self.chID = 0
        self.inScene = False
        self.Project = PywProject()

    def handle_starttag(self, tag, attrs):
        """ Get scene ID at scene start. """
        if tag == 'div':
            if attrs[0][0] == 'id':
                if attrs[0][1].count('ChID'):
                    self.chID = re.search('[0-9]+', attrs[0][1]).group()
                    self.Project.chapters[self.chID] = self.Project.Chapter()
                    self.Project.chapters[self.chID].scenes = []
                elif attrs[0][1].count('ScID'):
                    self.scID = re.search('[0-9]+', attrs[0][1]).group()
                    self.Project.scenes[self.scID] = self.Project.Scene()
                    self.Project.chapters[self.chID].scenes.append(self.scID)
                    self.inScene = True

    def handle_endtag(self, tag):
        """ Save scene content in dictionary at scene end. """
        if tag == 'div':
            if self.inScene:
                self.Project.scenes[self.scID].sceneContent = self.sceneText
                self.sceneText = ''
                self.inScene = False

    def handle_data(self, data):
        """ Collect paragraphs within scene. """
        if self.inScene:
            if data != ' ':
                self.sceneText = self.sceneText + data + '\n'
