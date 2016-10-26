#do a spellcheck and then parse the file

import spellcheck
import parser
from processData import toText, compileList
import sys, os

filePath = sys.argv[1]
outFilePath = sys.argv[2]
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
    key=i[0]
    field=i[1]
    if parser.isCheckmarkField(key):
        field=parser.processCheckmarkField(field)
        correctedFile.append([key, [spellcheck.correct(field)]])
    else:
        correctedFile.append([key, spellcheck.correctLine(field)])

#print the list
print("\ncorrected file:\n")
for i in correctedFile:
    print(i)

#output the list to a file
toText(outFilePath, compileList(correctedFile))
