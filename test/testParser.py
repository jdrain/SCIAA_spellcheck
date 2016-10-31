#test script for functions in the parser module

import parser, sys, os

filePath = sys.argv[1]
fileList = parser.readFile(filePath)
for i in fileList:
    print(i)
refinedFile = parser.looseLineListFilter(fileList)
for keys,values in refinedFile.items():
    print("\n")
    print(keys)
    print(values)
