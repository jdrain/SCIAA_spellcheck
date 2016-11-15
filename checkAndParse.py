#do a spellcheck and then parse the file

import textProcessing.spellcheck as spellcheck
import textProcessing.parser as parser
import textProcessing.processData as processData
import sys, os

filePath = sys.argv[1]
outFilePath = sys.argv[2]
csvFilePath = sys.argv[3]
fileList = parser.removeUnderlines(parser.readFile(filePath))

#print filename and contents
print("\nsource file: " + filePath + "\n")
for i in fileList:
    print(i)

#get key data from json files
checkmarkKeys=processData.processJSON("./textProcessing/checkmarkKeys.json")
keys=processData.processJSON("./textProcessing/keys.json")
checkmarkKeys=keys["1985_checkmark_keys"]
nextLineKeys=keys["1985_next_line_keys"]
multipleLineKeys=keys["1985_multiple_line_keys"]
keys=keys["1985_keys"]

#parse and print contents
print("\nrefined file:\n")
refinedFile =(
parser.looseLineListFilter(fileList,keys,nextLineKeys,multipleLineKeys)
)
for i in refinedFile:
    print(i)

#spellcheck the file
correctedFile = []
for i in refinedFile:
    key=i[0]
    field=i[1]
    if parser.isCheckmarkField(key,checkmarkKeys):
        field=parser.processCheckmarkField(field)
        correctedFile.append([key, [spellcheck.correct(field)]])
    else:
        correctedFile.append([key, spellcheck.correctLine(field)])

#print the list
print("\ncorrected file:\n")
for i in correctedFile:
    print(i)

#output the list to a text file
processData.toText(outFilePath, processData.compileList(correctedFile))

#output the list to a CSV file
processData.toCSV(csvFilePath, processData.compressList(correctedFile))
