#do a spellcheck and then parse the file

import spellcheck
import parser
import sys, os

filePath = sys.argv[1]
fileList = parser.readFile(filePath)

#print filename
print("\nsource file: " + filePath + "\n")

#correct the file
cFileList = spellcheck.correctFile(fileList)

print("\nfile corrected with technique one:\n")
for i in range(0, len(cFileList)):
    print(cFileList[i])

#print the differences between the two files
print(spellcheck.diffCount(fileList, cFileList))

#parse portion
refinedFile = parser.looseLineListFilter(cFileList)
for keys,values in refinedFile.items():
    print("\n")
    print(keys)
    print(values)
