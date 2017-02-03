import csv
import json

"""
function: parse csv into 2D file list
"""
def readCSV(filepath):
    csv_list=[]
    with open(filepath, 'rb') as csvfile:
        reader=csv.reader(csvfile,delimiter=',')
        for row  in reader:
            csv_list.append(row)
    return csv_list

"""
function: process json data from file
"""
def processJSON(filepath):
    data=json.load(open(filepath))
    return data
"""
function: compile list of form [['key', ['word1', 'word2']], ...]
down to [['key word1 word2]]
"""
def compileList(data):
    ls = []
    for i in data:
        if len(i[1])==1:
            ls.append("\n"+str(i[0])+"\n"+str(i[1][0])+"\n")
        else:
            ls.append("\n"+str(i[0])+"\n"+" ".join(i[1])+"\n")
    return ls
"""
function: compress list of form [['key', ['word1', 'word2']], ...]
down to [['key', 'word1 word2'],...]
"""
def compressList(data):
    ls=[]
    for i in data:
        if len(i[1])==1:
            ls.append([i[0], i[1][0]])
        else:
            ls.append([i[0], " ".join(i[1])])
    return ls
"""
function: compress list of the form [['key','w1',...'wn']..]
down to [['key', 'w1 ... wn']...]
"""
def compress_list(data):
    ls=[]
    for i in data:
        i=[str(j) for j in i]
        if len(i)>2:
            ls.append([i[0]," ".join(i[1:len(i)-1])])
        else:
            ls.append(i)
    return ls

"""
function: write a list back to a text file
"""
def toText(path, data):
    f=open(path, 'w')
    for i in data:
        f.write(i)
    f.close()

"""
function: write a list back to a CSV file
"""
def toCSV(path, data):
    with open(path, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for i in data:
            writer.writerow(i)
"""
function: log the data going into the db
"""
def get_db_log(file_ls,logfile):
    #file_ls is like [["x:","y z"],[...],...]
    with open(logfile,"w") as outfile:
        for i in file_ls:
            j=" ".join(str(i))+"\n"
            outfile.write(j)
"""
function: write a processed list to a SCIAA database formatted csvOut
"""
def write_to_dbf(filename, output_ls, db_field_coords, csv_out, dbf_out_path, match_using_filename=True):
    """
    use filename to find column
    parse filepath:
        -split over '/' and take last element
        -split over '_' and take first element
    """
    print("test1")
    #parse filename
    f0=filename.split("/")
    f1=f0[len(f0)-1]
    fp=f1.split("_")[0]

    #find the row
    row=None
    id_col=4 #column with file ID in it
    date_col=7 #column with the date in it

    #set date_exists, date fields
    date_exists=False
    date=None
    for i in output_ls:
        if i[0]=="RECORDEDDA":
            print("date exists")
            date_exists=True
            date=i[1]

    if (match_using_filename and date_exists):
        for i in range(0,len(csv_out)):
            if csv_out[i][4]==fp and csv_out[i][7]==date:
                print("\nPATH MATCH FOUND!")
                print("\nBased on: Date and fp")
                row=i
                break
    if (date_exists and row==None):
        for i in range(0,len(csv_out)):
            if csv_out[i][date_col]==date:
                print("\nPATH MATCH FOUND!")
                print("\nBased on: Date")
                row=i
                break
    if (match_using_filename and row==None):
        for i in range(0,len(csv_out)):
            if csv_out[i][4]==fp:
                print("\nPATH MATCH FOUND!")
                print("\nBased on: fp")
                row=i
                break

    if row==None:    
        print("Match using fname was: ")
        print(match_using_filename)
        print("No match found")
        return

    else:
        for i in output_ls:
            print("i[0] is: "+str(i[0]))
            out_key=db_field_coords[i[0]]
            print("writing to: ["+str(row)+"]["+str(out_key)+"]")
            csv_out[row][out_key]=i[1]

    #write to file
    toCSV(dbf_out_path,csv_out)

"""
function: slice the CSV based on certain columns. May be useful just for viewability
"""
def get_csv_columns(columns, csv_fp):
    #pass the columns as integers in a list
    csv_file_ls = readCSV(csv_fp)
    sliced_ls = [[i[j] for i in csv_file_ls] for j in columns]
    return sliced_ls

"""
function: get pertinent columns from a json
"""
def get_pertinent_columns(pertinent_fields_json):
    data = processJSON(pertinent_fields_json)
    cols = [data[key] for key in data.keys()]
    return cols
