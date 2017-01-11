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
