#do a spellcheck and then parse the file

import spellcheck
import parser
import sys, os

filePath = sys.argv[1]
fileList = parser.readFile(filePath)

#print filename and contents
print("\nsource file: " + filePath + "\n")
for i in fileList:
    print(i)

#parse and print contents
print("\nrefined file:\n")
refinedFile = parser.looseLineListFilter(fileList)
for i in refinedFile:
    print(i)

#spellcheck the file
correctedFile = []
for i in refinedFile:
    correctedFile.append([i[0], spellcheck.correctLine(i[1])])

print("\nspellchecked:\n")
for i in correctedFile:
    print(i)
