#do a spellcheck and then parse the file

import spellcheck
import parser
import sys, os

"""
TODO:
    -Need to fix the spellchecking on the dictionary
"""

filePath = sys.argv[1]
fileList = parser.readFile(filePath)

#print filename
print("\nsource file: " + filePath + "\n")

#correct the file
#cFileList = spellcheck.correctFile(fileList)

#print("\nfile corrected with technique one:\n")
#for i in range(0, len(cFileList)):
#    print(cFileList[i])

#print the differences between the two files
#print(spellcheck.diffCount(fileList, cFileList))

#parse and spellcheck
refinedFile = parser.looseLineListFilter(fileList)
for value in refinedFile.items():
    value = spellcheck.correctLine(value)
    print(value)

for keys,values in refinedFile.items():
    print(keys)
    print(values)
