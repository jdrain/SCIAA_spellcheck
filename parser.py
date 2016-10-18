#parser to extract pertinent information from raw text files

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

"""
We need:
    -a function to recognize key expressions
    -a list of the key expressions
"""
keys=[
      ["descriptive", "site", "type"],["prehistoric"],["historic"],
      ["archaeological", "investigation"],["level", "of", "significance"],
      ["justification"],["landform", "location"],["site"],
      ["elevation"],["on", "site","soil", "type"],
      ["soil", "classification"],["major", "river", "system"],
      ["nearest", "river/stream"],["estimated", "site", "dimensions"],
      ["site", "depth"],["cultural", "features"],
      ["general", "site", "description"]
     ]

"""
function: to read files into a list
input: file path
output: list with each element a string corresponding to one line from
the file
"""
def readFile(path):
    f = file(path)
    fileList = []
    for line in f:
        if line != "\n":
            line = line.lower()
            ls = line.split()
            fileList.append(ls)
    return fileList

"""
function: to detect a substring within another string
input: a string and then a substring to be searched for
output: a boolean based on whether or not that substring was found
"""
def detectSubstring(substring, string):
    stringLen = len(string)
    substringLen = len(substring)
    if substringLen > stringLen:
        return False
    elif substring in string:
        return True
    else:
        return False

"""
function: to loop through the file and find lines with pertinent
information
input: file list and a list of key substrings
output: processed file list
"""
def findLines(fileList):
    keyCopy = keys #copy the list of keys
    fileList.sort() #sort the fileList
    refinedFile = []
    for i in keyCopy:
        for j in fileList:
            substringFound = False
            while (substringFound == False):
                if (detectSubstring(i, j) == True):
                    refinedFile.append(j)
                    keyCopy.remove(i)
                    substringFound = True
    return refinedFile

"""
function: filter a lineList and try to find
"""
def lineListFilter(lineList):
    dic={}
    for i in lineList:
        for j in keys:
            k=0
            while (k<len(i) and i[k]!=j[0]):
                initRat = fuzz.ratio(i[k], j[0])
                print("ratio: ")
                print(initRat)
                print("i[k]:")
                print(i[k])
                print("j[0]:")
                print(j[0])
                if (initRat >= 80):
                    print("found potential match\n")
                    #concatenate and implement fuzzyfind
                    keyStr = " ".join(j)
                    lineStr = " ".join(i[k:(k+len(j))])
                    ratio = fuzz.ratio(keyStr, lineStr)
                    partialRatio = fuzz.ratio(keyStr, lineStr)
                    print("ratio: ")
                    print(ratio)
                    print("partial ratio: ")
                    print(partialRatio)
                    if ratio >= 80 or partialRatio >= 80:
                        dic[keyStr]=i
                k+=1
    return dic
"""
function: filter a lineList and try to find a match, but less rigorously
TODO:
    -make more rigorous once it's working
"""
def looseLineListFilter(lineList):
    dic={}
    for i in keys:
        for j in lineList:
            potentialMatchFound=False
            foundInd=-1
            k=0
            while(k<len(j) and potentialMatchFound==False):
                if fuzz.ratio(str(j[k]), str(i[0])) >= 70:
                    potentialMatchFound=True
                    foundInd=k
                k+=1
            if potentialMatchFound==True:
                #call new method
                if checkForKey(j,i,foundInd)==True:
                    dic[" ".join(i)]=" ".join(j)
    return dic
"""
function: loop through a line and see if it contains a key
"""
def checkForKey(line, key, startInd):
    Matched=True
    i=startInd
    j=0
    while (i<startInd+len(key) and i<len(line) and Matched==True):
        if fuzz.ratio(str(line[i]), str(key[j])) < 70:
            Matched=False
        i+=1
        j+=1
    if Matched==True:
        return True
    else:
        return False
