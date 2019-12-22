""" PyWriter module

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import re
from pywriter.html.htmlparser import PywHTMLParser
from pywriter.project import PywProject


def html_to_yw7(htmlFile, yw7File):
    """ Convert html into yw7 sceneContents and modify .yw7 file. """

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
        with open(htmlFile, 'r', encoding='utf-8') as f:
            text = (f.read())
    except:
        try:
            with open(htmlFile, 'r') as f:
                text = (f.read())
        except(FileNotFoundError):
            return('\nERROR: "' + htmlFile + '" not found.')

    text = format_yw7(text)

    parser = PywHTMLParser()
    parser.feed(text)
    prj = PywProject(yw7File)

    return(prj.write_scene_contents(parser.get_scene_contents()))


if __name__ == '__main__':
    pass
