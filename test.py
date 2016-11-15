import textProcessing.parser as parser
import textProcessing.processData as processData
import sys, os
from textProcessing import processData

filePath=sys.argv[1]
csvPath=sys.argv[2]
fileList=parser.read_file_simple(filePath)

print("\nsource file: "+filePath+"\n")
for i in fileList:
    print(i)

#get data from json
keys=processData.processJSON("./textProcessing/keys1.json")

#print keys for debug
for key in keys:
    print(key)

#parse
parsed=parser.filter_potential_data(keys["1985"],fileList)
extracted=parser.extract_data(fileList,parsed,keys["1985"])

#print results
print("\nparsed: \n")
for i in parsed:
    print(i)

print("\nextracted: \n")
for i in extracted:
    print(i)

#compress and write to file
print("\ncompressing and writing to file\n")
compressed=processData.compress_list(extracted)
processData.toCSV(csvPath,compressed)
