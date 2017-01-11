import textProcessing.parser as parser
import textProcessing.processData as processData
import sys, os
from textProcessing import processData

"""
TODO:
    -add function to get the type of form
    -change code to add to the csv instead of creating a new one
"""

filePath=sys.argv[1]
csvPath=sys.argv[2]
fileList=parser.read_file_simple(filePath)

print("\nsource file: "+filePath+"\n")

#get data from json
keys=processData.processJSON("./textProcessing/keys1.json")
encoding_keys=processData.processJSON("./textProcessing/Encodings.json")
#print keys for debug
"""
for key in keys:
    print(key)
"""

#parse
print("\nparser is removing underlines: \n")
fileList=parser.remove_underlines(fileList)

print("\nparser is removing newline nums: \n")
fileList=parser.remove_newline_nums(fileList)

print("\nparser is choosing best matches: \n")
parsed=parser.filter_potential_data(keys["1985"],fileList)

#print results
print("\nparsed: \n")
for i in parsed:
    print(i)

extracted=parser.extract_data(fileList,parsed,keys["1985"])

print("\nextracted: \n")
for i in extracted:
    print(i)

formatted=parser.database_format(extracted,keys["1985"],encoding_keys)

print("\nformatted: \n")
for i in formatted:
    print(i)

#compress and write to file
print("\ncompressing and writing to file\n")
compressed=processData.compress_list(formatted)
processData.toCSV(csvPath,compressed)
