#test script for functions in the parser module

import parser, sys, os

filePath = sys.argv[1]
fileList = parser.readFile(filePath)
refinedFile = parser.findLines(fileList)
for i in refinedFile:
    print("\n")
    print(i)
