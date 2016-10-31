import csv

"""
data will come in as a list
"""

"""
function: compile list of form [['key', ['word1', 'word2']], ...]
down to [['key word1 word2]]
"""
def compileList(data):
    ls = []
    for i in data:
        if len(i[1])==1:
            ls.append("\n"+i[0]+"\n"+i[1][0]+"\n")
        else:
            ls.append("\n"+i[0]+"\n"+" ".join(i[1])+"\n")
    return ls
"""
function: compress list of form [['key', ['word1', 'word2']], ...]
down to [['key', 'word1 word2']]
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
function: write the list back to a text file
"""
def toText(path, data):
    f=open(path, 'w')
    for i in data:
        f.write(i)
    f.close()

"""
function: write the list back to a CSV file
"""
def toCSV(path, data):
    with open(path, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for i in data:
            writer.writerow(i)
