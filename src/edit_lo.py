""""Write yWriter scene content directly to LibreOffice

This script is used to test UNO access for the 
yW2OO v3 Python macro. 

"""
import os
import uno
from subprocess import Popen
from time import sleep
from pywriter.model.yw7file import Yw7File


FILENAME = 'normal.yw7'
HEADING_STYLES = ('Heading 2', 'Heading 1')
SCENE_DIVIDER = '* * *'

LIBREOFFICE = ['c:/Program Files/LibreOffice/program/swriter.exe',
               'c:/Program Files (x86)/LibreOffice/program/swriter.exe',
               'c:/Program Files/LibreOffice 5/program/swriter.exe',
               'c:/Program Files (x86)/LibreOffice 5/program/swriter.exe']

SOCKET = 'socket,host=localhost,port=8100,tcpNoDelay=1;urp;'


def main():
    """Test Libreoffice API access
    see: https://www.linux-magazin.de/ausgaben/2016/05/libre-office-testen/2/
    """
    novel = Yw7File(FILENAME)
    novel.read()

    # start LibreOffice
    try:
        for lo in LIBREOFFICE:

            if os.path.isfile(lo):
                cmd = [os.path.normpath(lo)]
                cmd.append('--writer')
                cmd.append('--accept=' + SOCKET)
                app = Popen(cmd)

    except Exception as e:
        raise Exception("ERROR: can't start LibreOffice: %s" % e.message)

    if app.pid <= 0:
        raise Exception("ERROR: can't start LibreOffice.")

    # establish connection to LibreOffice
    context = uno.getComponentContext()
    resolver = context.ServiceManager.createInstanceWithContext(
        'com.sun.star.bridge.UnoUrlResolver',
        context)

    n = 0
    while n < 12:

        try:
            context = resolver.resolve(
                'uno:' + SOCKET + 'StarOffice.ComponentContext')
            break

        except:
            pass

        sleep(0.5)
        n += 1

    desktop = context.ServiceManager.createInstanceWithContext(
        'com.sun.star.frame.Desktop', context)

    if not (desktop):
        raise Exception("ERROR: can't create LibreOffice desktop.")

    # from here on, LibreOffice is controlled via the connection

    # access the current writer document
    model = desktop.getCurrentComponent()

    # access the document's text property
    text = model.Text

    # create a cursor
    cursor = text.createTextCursor()

    for chId in novel.srtChapters:

        if (not novel.chapters[chId].isUnused) and novel.chapters[chId].chType == 0:
            cursor.ParaStyleName = HEADING_STYLES[novel.chapters[chId].chLevel]
            text.insertString(cursor, novel.chapters[chId].title, 0)
            text.insertControlCharacter(cursor, uno.getConstantByName(
                "com.sun.star.text.ControlCharacter.PARAGRAPH_BREAK"), 0)
            firstParagraph = True

            for scId in novel.chapters[chId].srtScenes:

                if not novel.scenes[scId].isUnused:

                    if not firstParagraph:
                        cursor.ParaStyleName = 'Heading 4'
                        text.insertString(cursor, SCENE_DIVIDER, 0)
                        text.insertControlCharacter(cursor, uno.getConstantByName(
                            "com.sun.star.text.ControlCharacter.PARAGRAPH_BREAK"), 0)

                    if novel.scenes[scId].sceneContent is not None:
                        lines = novel.scenes[scId].sceneContent.split('\n')
                        cursor.ParaStyleName = 'Text body'

                        for line in lines:
                            text.insertString(cursor, line, 0)
                            text.insertControlCharacter(cursor, uno.getConstantByName(
                                "com.sun.star.text.ControlCharacter.PARAGRAPH_BREAK"), 0)
                            cursor.ParaStyleName = 'First line indent'

                        firstParagraph = False


if __name__ == '__main__':
    main()
