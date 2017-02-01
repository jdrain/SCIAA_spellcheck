import textProcessing.parser as parser
import textProcessing.processData as processData
import sys, os
from textProcessing import processData

"""
TODO:
    -add function to get the type of form
"""

#input dir and output path
dir_path=sys.argv[1]
dbf_csv_path=sys.argv[2]

#get data from json files
keys=processData.processJSON("./textProcessing/JSONdata/explicit_keys.json")
encoding_keys=processData.processJSON("./textProcessing/JSONdata/Encodings.json")
db_field_coordinates=processData.processJSON("./textProcessing/JSONdata/DatabaseFieldCoordinates.json")
date_conversions=processData.processJSON("./textProcessing/JSONdata/DateConversion.json")

overall=[]
for fpath in os.listdir(dir_path):

    fileList=parser.read_file_simple(dir_path+"/"+fpath)
    csvOut=processData.readCSV(dbf_csv_path)

    print("\nsource file: "+fpath+"\n")

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

    formatted=parser.database_format(extracted,keys["1985"],encoding_keys,date_conversions)

    print("\nformatted: \n")
    for i in formatted:
        print(i)

    #compress and write to file
    print("\ncompressing:\n")
    compressed=processData.compress_list(formatted)
    for i in compressed:
        overall.append(i)

    #writing to the dbf csv
    print("\nwriting to dbf file:")
    processData.write_to_dbf(fpath,compressed,db_field_coordinates,csvOut,dbf_csv_path)

print("\nlogging:\n")
processData.get_db_log(overall,"lastRun.txt")
