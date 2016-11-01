#parser to extract pertinent information from raw text files

from fuzzywuzzy import fuzz

"""
TODO:
    -Fix the recognition of 'excavation' as 'elevation
    -How do we cope with noise in these checkmark fields?
    -Remove the underline characters
"""

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
def findLines(fileList,keys):
    keyCopy=keys
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
def lineListFilter(lineList,keys):
    dic={}
    for i in lineList:
        for j in keys:
            k=0
            while (k<len(i) and i[k]!=j[0]):
                initRat = fuzz.ratio(i[k], j[0])
                if (initRat >= 80):
                    #concatenate and implement fuzzyfind
                    keyStr = " ".join(j)
                    lineStr = " ".join(i[k:(k+len(j))])
                    ratio = fuzz.ratio(keyStr, lineStr)
                    partialRatio = fuzz.ratio(keyStr, lineStr)
                    if ratio >= 80 or partialRatio >= 80:
                        dic[keyStr]=i
                k+=1
    return dic
"""
function: filter a lineList and try to find a match, but less rigorously
TODO:
    -make more rigorous once it's working
"""
def looseLineListFilter(lineList,keys):
    ls = []
    for i in keys:
        for j in lineList: 
            potentialMatchFound=False
            foundInd=-1
            k=0
            #keep iterating until a potential match is found or
            #the list is done
            while(k<len(j) and potentialMatchFound==False):
                rat = fuzz.ratio(str(j[k]), str(i[0]))
                if rat >= 70:
                    potentialMatchFound=True
                    foundInd=k
                k+=1
            #if we find a potential match, check that it is in fact
            #a match
            if potentialMatchFound==True:
                #call new method
                if checkForKey(j,i,foundInd)==True:
                    ls.append([" ".join(i),j, rat])
    return determineBestMatch(ls)

"""
function: filter through a list and check for the best match; helper
method for looseLineListFilter
"""
def determineBestMatch(ls):
    i=0
    ls1 = []
    lsLen = len(ls)
    #go through the whole list
    while (i<lsLen):
        bestRatio=0
        startInd=i
        currentKey=ls[i][0]
        ls2=[currentKey]
        #we have multiple matches for certain keys. Loop and determine
        #which is the best one
        while (i<lsLen and ls[i][0] == currentKey):
            if ls[i][2] > bestRatio:
                bestRatio = ls[i][2]
            i+=1
        #now choose the best one
        for j in range(startInd, i):
            if ls[j][2] == bestRatio:
                ls2.append(ls[j][1])
        ls1.append(ls2)
    return ls1
"""
function: loop through a line and see if it contains a key
"""
def checkForKey(line,keys,startInd):
    Matched=True
    i=startInd
    j=0
    #Make sure that subsequent words in a line match the key
    while (i<startInd+len(keys) and i<len(line) and Matched==True):
        if fuzz.ratio(str(line[i]), str(keys[j])) < 70:
            Matched=False
        i+=1
        j+=1
    if Matched==True:
        return True
    else:
        return False
"""
function: determine if a line contains a checkmark field
"""
def isCheckmarkField(fieldName,keys):
    for key in keys:
        if fuzz.ratio(fieldName, key)>=70:
            return True
"""
function: process a line that contains a checkmark field
    -add functionality to differentiate between noise and legimate text
    (give precedence to an x)
"""
def processCheckmarkField(line):
    val=''
    i=0
    found=False
    alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789'
    while i<len(line)-1 and found==False:
        if len(line[i+1])==1 and line[i+1] in alphabet:
            val=line[i]
            found=True
        else:
            i+=1
    return val

