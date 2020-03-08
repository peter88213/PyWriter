import os


def run(sourcePath):

    scriptPath = os.environ['USERPROFILE'] + '\\AppData\\Roaming\\OpenOffice.org\\3\\user\\Scripts\\python\\'

    argument1 = scriptPath + 'saveyw7.bat'
    argument2 = sourcePath

    cmd = argument1 + ' \"' + argument2 + '\"'

    status = os.system(cmd)

    if status == 0:
        return 'SUCCESS: Data written back to yw7.'

    else:
        return 'ERROR occurred during execution of ' + cmd


if __name__ == '__main__':
    pass