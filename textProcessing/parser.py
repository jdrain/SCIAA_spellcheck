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
        line = line.lower()
        ls = line.split()
        fileList.append(ls)
    return fileList
"""
function: read a file into a one dimension list of words
"""
def read_file_simple(path):
    f=file(path)
    fileList=[]
    for line  in f:
        line=line.lower()
        ls=line.split()
        for i in ls:
            fileList.append(i)
        fileList.append("\n")
    return fileList
"""
function: extract indices where info associated with certain keys will
start and end, as well as the fuzz ratio of that key
"""
def filter_potential_data(keys,file_list):
    for key in keys.keys():
        print(keys[key][0])
    ls=[]
    for key in keys.keys():
        for i in find_keys(keys[key][0],file_list,keys[key][1]):
            ls.append(i)
    return ls
"""
function: help find keys
ls is of the form: [[key, startInd, finalInd, fuzz ratio]...]
"""

def find_keys(key,file_list,end):
    ls1=[]
    for i in range(0,len(file_list)):
        if fuzz.ratio(str(file_list[i]),str(key[0]))>=80:
            #start iterating
            print("iterating")
            j=i+1
            k=1
            not_found=False
            while k<len(key) and not_found==False:
                if fuzz.ratio(str(file_list[j]),str(key[k]))<80:
                    not_found=True
                j+=1
                k+=1
            rat=fuzz.ratio(" ".join(file_list[i:j])," ".join(key))
            if not_found==False:
                print("found start")
                ls=[]
                ls.append(" ".join(key))
                ls.append(j)
                #take data from j until we find the end key
                found_end=False
                while(found_end==False and j<len(file_list)):
                    if fuzz.ratio(str(file_list[j]),str(end[0]))>80:
                        #start checking
                        potential_match=True
                        l=1
                        while potential_match==True and l<len(end):
                            if fuzz.ratio(str(end[l]),str(file_list[j+l]))<70:
                                potential_match=False
                            l+=1
                        if potential_match==True:
                            print("found end")
                            found_end=True
                            ls.append(j)
                            ls.append(rat)
                            ls1.append(ls)
                    j+=1
    return ls1
"""
function: extract the actual data once it has been filtered
"""
def extract_data(file_list,filtered_data,keys):
    nums=["1","2","3","4","5","6","7","8","9","0"]
    i=0
    ls=[]
    while i<len(filtered_data):
        if len(filtered_data[i])!=4:
            i+=1
        else:
            start=filtered_data[i][1]
            end=filtered_data[i][2]
            key=filtered_data[i][0]
            #add filtering for checkmarked fields and whatnot here
            #what even are these keys...
            if (keys[key][2][0]==False and keys[key][3][0]==False and
                    keys[key][4][0]==False):
                ls.append([key,
                " ".join(remove_new_lines(file_list[start:end]))])
            else:
                #is the field on the next line or multiple lines?
                if keys[key][2][0]==True or keys[key][4][0]==True:
                    #ignore newline chars
                    print("ignoring newlines\n")
                    ls.append([key," ".join(file_list[start:end])])
                #is the field a checked field?
                if keys[key][3][0]==True:
                    #deal with checked fields
                    print("found a checked field!")
                    ls.append(process_checked_field(file_list,key,start,end))
        i+=1
    return remove_extra_chars(ls,keys,nums)
"""
function: deal with checked fields
"""
def process_checked_field(file_list,key,start,end):
    ls1=[]
    ls1.append(key)
    for j in range(start,end):
        print("element "+str(j)+": "+str(file_list[j]))
        if (j!=0 and len(file_list[j])==1 and
        file_list[j] != "\n" and len(file_list[j-1])!=1):
            print("found a checked option")
            ls1.append(file_list[j-1])
    return ls1
"""
function: remove extraneous chars from data that may have gotten through
previous filtering
"""
def remove_extra_chars(file_list,keys,nums):
    ls=file_list
    for i in range(0, len(ls)):
        #index 0 is the key
        key=ls[i][0]
        print("current key: "+str(key))
        if keys[key][6][0]==True:
            print("found non-numeric entry: "+str(key))
            print("current entry: "+str(ls[i]))
            #process out numeric data
            for j in range(1,len(ls[i])):
                for num in nums:
                    ls[i][j]=str(ls[i][j]).replace(num,"")
            print("final entry: "+str(ls[i]))
        elif keys[key][5][0]==True:
            print("found numeric entry: "+str(key))
            print("current entry: "+str(ls[i]))
            #process out non-numeric data
            for j in range(1,len(ls[i])):
                for char in ls[i][j]:
                    if char not in nums:
                        ls[i][j]=ls[i][j].replace(char,"")
            print("final entry: "+str(ls[i]))
    return ls
"""
function: remove new line chars
"""
def remove_new_lines(file_list):
    for i in range(0, len(file_list)):
        file_list[i]=file_list[i].replace("\n","")
    return file_list


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
def looseLineListFilter(lineList,keys,nextLineKeys,multipleLineKeys):
    ls = []
    for i in keys:
        for j in range(0,len(lineList)): 
            potentialMatchFound=False
            foundInd=-1
            k=0
            #keep iterating until a potential match is found or
            #the list is done
            while(k<len(lineList[j]) and potentialMatchFound==False):
                rat = fuzz.ratio(str(lineList[j][k]), str(i[0]))
                if rat >= 70:
                    potentialMatchFound=True
                    foundInd=k
                k+=1
            #if we find a potential match, check that it is in fact
            #a match
            if potentialMatchFound==True:
                #call new method
                #insert support for multiple and next line fields here!
                if (checkForKey(lineList[j],i,foundInd)==True and
                isNextLineField(i,nextLineKeys)==True):
                    ls.append([
                    " ".join(i),nextLineField(lineList,j),rat
                    ])
                elif (checkForKey(lineList[j],i,foundInd)==True and
                isMultipleLineField(i,multipleLineKeys)==True):
                    ls.append([
                    " ".join(i),multipleLineField(lineList,j),rat
                    ])
                elif checkForKey(lineList[j],i,foundInd)==True:
                    ls.append([" ".join(i),lineList[j], rat])
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
function: extract data from a line
"""

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
    return False
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
    if val=='':
        return " ".join(line)
    else:
        return val
""""
function: determine in a line contains a circle field
"""
def isCircleField(field,circleKeys):
    for key in circleKeys:
        if fuzz.ratio(field,key)>=70:
            return True
    return False
"""
function: deal with circled fields
"""
def processCircleField(line):
    val=''
    i=1
    found=False
    alphabet='abcdefghijklmnopqrstuvwxyz0123456789'
    while i<len(line)-1 and found==False:
        if (len(line[i+1])==1 and len(line[i-1])==1 and line[i+1] in
        alphabet and line[i-1] in alphabet):
            val=line[i]
            found=True
        else:
            i+=1
    if val=='':
        return " ".join(line)
    else:
        return val
"""
function: determine if a field is one of those that contains multiple
lines
"""
def isMultipleLineField(field, multipleLineKeys):
    for key in multipleLineKeys:
        if fuzz.ratio(field,key)>=90:
            return True
    return False
"""
function: deal with fields that are multiple lines
"""
def multipleLineField(lineList,currentInd):
    #take the next five lines
    ls=lineList[currentInd]
    if len(lineList)-currentInd < 5:
        ls1=lineList[currentInd:len(lineList)-1]
    else:
        ls1=lineList[currentInd:currentInd+5]
    i=1
    currentInd+=1
    while i<5 and currentInd<len(lineList) and lineList[currentInd]:
        for j in lineList[currentInd]:
            ls.append(j)
        i+=1
        currentInd+=1
    return ls
"""
function: determine if a field is on the next line
"""
def isNextLineField(field, nextLineKeys):
    for key in nextLineKeys:
        if fuzz.ratio(field,key)>=70:
            return True
    return False
"""
function: deal with fields that are on the next line
"""
def nextLineField(lineList,currentInd):
    #just take the next line
    if lineList[currentInd+1]:
        return lineList[currentInd+1]
    else:
        return []
"""
function: remove underlines from the files
"""
def removeUnderlines(filelist):
    ls=[]
    for i in filelist:
        ls1=[]
        for j in i:
            j=j.replace("_"," ")
            j=j.replace("-"," ")
            ls1.append(j)
        ls.append(ls1)
    return ls

