'''
Created on 23.12.2019

@author: Peter
'''
import re

TEST_PROJECT = 'yw7 Sample Project'

TEST_PATH = '../test/'
TEST_EXEC_PATH = 'yw7/'
TEST_DATA_PATH = 'data/'

YW7_FILE = TEST_PROJECT + '.yw7'

file = TEST_PATH + TEST_EXEC_PATH + YW7_FILE

with open(file, 'r') as f:
    lines = f.readlines()

cdataTags = []

for line in lines:
    tag = re.search('\<(.+?)\>\<\!\[CDATA', line)
    if tag is not None:
        if not (tag.group(1) in cdataTags):
            cdataTags.append(tag.group(1))

print(cdataTags)
