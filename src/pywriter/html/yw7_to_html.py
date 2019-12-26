""" PyWriter module

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.project import PywProject

HEADING_MARKER = ("h2", "h1")


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
                for scID in prj.chapters[chID].scene:
                    f.write(scID + ',"')
                    for line in prj.scenes[scID].desc:
                        f.write(line.replace('"', "'"))
                    f.write('"\n')

    sceneDivider = '* * *'

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

    prj = PywProject(yw7File)
    htmlText = htmlHeader.replace('$bookTitle$', prj.projectTitle)
    for chID in prj.chapters:
        htmlText = htmlText + '<div id="ChID:' + chID + '">\n'
        headingMarker = HEADING_MARKER[prj.chapters[chID].type]
        htmlText = htmlText + '<' + headingMarker + '>' + \
            format_chapter_title(
                prj.chapters[chID].title) + '</' + headingMarker + '>\n'
        for scID in prj.chapters[chID].scenes:
            htmlText = htmlText + '<h4>' + sceneDivider + '</h4>\n'
            htmlText = htmlText + '<div id="ScID:' + scID + '">\n'
            htmlText = htmlText + '<p class="textbody">'
            htmlText = htmlText + '<a name="ScID:' + scID + '" />'
            # Insert scene ID as anchor.
            htmlText = htmlText + '<!-- ' + prj.scenes[scID].title + ' -->\n'
            # Insert scene title as comment.
            try:
                htmlText = htmlText + \
                    format_yw7(prj.scenes[scID].get_sceneContent())
            except(TypeError):
                htmlText = htmlText + ' '
            htmlText = htmlText + '</p>\n'
            htmlText = htmlText + '</div>\n'

        htmlText = htmlText + '</div>\n'
    htmlText = htmlText.replace(
        '</h1>\n<h4>' + sceneDivider + '</h4>', '</h1>')
    htmlText = htmlText.replace(
        '</h2>\n<h4>' + sceneDivider + '</h4>', '</h2>')
    htmlText = htmlText + htmlFooter

    try:
        with open(htmlFile, 'w', encoding='utf-8') as f:
            f.write(htmlText)
    except(PermissionError):
        return('\nERROR: ' + htmlFile + '" is write protected.')

    #create_csv(prj, htmlFile)

    return('\nSUCCESS: ' + str(len(prj.scenes)) + ' Scenes written to "' + htmlFile + '".')


if __name__ == '__main__':
    pass
