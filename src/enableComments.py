"""Make LibreOffice Writer >6.3 import HTML comments

As of version 6.4, LibreOffice Writer ignores HTML comments by default.
This script modifies 'registrymodifications.xcu' in order to enable 
the conversion of HTML comments to ODT comments upon HTML import.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os


CONFIG_FILE = os.environ['USERPROFILE'] + \
    '\\AppData\Roaming\\LibreOffice\\4\\user\\registrymodifications.xcu'


def main():
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            text = f.read()

    except:
        print('"' + CONFIG_FILE + '" not found.')
        return

    if not 'HTML"><prop oor:name="IgnoreComments"' in text:

        # Add a user specific registry entry to override default behaviour.

        text = text.replace(
            '</oor:items>', '<item oor:path="/org.openoffice.Office.Writer/Filter/Import/HTML"><prop oor:name="IgnoreComments" oor:op="fuse"><value>false</value></prop></item>\n</oor:items>')

    elif 'HTML"><prop oor:name="IgnoreComments" oor:op="fuse"><value>true' in text:

        # Change the value of an already existing registry entry.

        text = text.replace('HTML"><prop oor:name="IgnoreComments" oor:op="fuse"><value>true',
                            'HTML"><prop oor:name="IgnoreComments" oor:op="fuse"><value>false')

    else:
        print('HTML comment conversion is already enabled.')
        return

    i = 0
    extension = '.bak'
    while os.path.isfile(CONFIG_FILE + extension + str(i)):
        i = i + 1

    extension = extension + str(i)
    os.rename(CONFIG_FILE, CONFIG_FILE + extension)

    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        f.write(text)

    print('"' + CONFIG_FILE +
          '" modified to enable HTML comment conversion.')


if __name__ == '__main__':
    main()
