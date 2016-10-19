#python module to implement a spellcheck
#NOT MY OWN
#from https://github.com/mattalcock/blog/blob/master/2012/12/5/python-spell-checker.rst

import re, collections

def words(text):
    return re.findall('[a-z]+', text.lower())

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

NWORDS = train(words(file('textFiles/Big.txt').read()))
alphabet = 'abcdefghijklmnopqrstuvwxyz1234567890'
numbers = '0123456789'
specialChars = '!@#$%^&*()_-+=?'
chars=['/',',',';','\'']

def edits1(word):
    s = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes    = [a + b[1:] for a, b in s if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in s if len(b)>1]
    replaces   = [a + c + b[1:] for a, b in s for c in alphabet if b]
    inserts    = [a + c + b     for a, b in s for c in alphabet]
    return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words):
    return set(w for w in words if w in NWORDS)

#Use this at the top level to correct a word
def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)

"""
MY OWN CODE BELOW THIS LINE

TODO:
    -Improve the processing of numbers by considering numbers with
    extraneous chars around them
    -Improve the processing of strings with colons at the end
    -Maybe we should consider just leaving strings of junk alone; the
    approach to solving seems to be doing more harm than good currently
"""

"""
function: read in file
"""
def readFile(path):
    f = file(path)
    fileList = []
    for line in f:
        if line != "\n":
            line = line.lower()
            ls = line.split()
            if line != []:
                fileList.append(ls)
    return fileList
"""
function: correct the file
"""
def correctFile(fileList):
    ls1 = []
    for i in fileList:
        ls1.append(correctLine(i))
    return ls1
"""
function: correct the file with a different technique
"""
def correctFileTwo(fileList):
    ls=[]
    for i in fileList:
        ls.append(correctLineTwo(i))
    return ls
"""
function: correct a line with another technique
"""
def correctLineTwo(line):
    newLine= []
    i = 0
    line=removeSpecialChars(line)
    while i<len(line):
        if isJunkString(line[i]):
            i+=1
        elif isNum(line[i]):
            newLine.append(line[i])
            i+=1
        elif hasInternalJunk(line[i]):
            c=correctChars(line[i])
            if c != line[i]:
                newLine.append(c)
            else:
                processed=processInternalJunk(line[i])
                for j in processed:
                    newLine.append(correct(j))
            i+=1
        elif hasSpecialChars(line[i]):
            c=correctChars(line[i])

        else:
            c=correct(line[i])
            newLine.append(c)
            i+=1
    return newLine
"""
function: correct a whole line
"""
def correctLine(line):
    newLine = []
    i = 0
    while i<len(line):
        if isJunkString(line[i]):
            i+=1
        elif isNumTwo(line[i]):
            newLine.append(line[i])
            i+=1
        elif hasInternalJunk(line[i]):
            #try to correct the word as if it has special chars first
            c=correctChars(line[i])
            if c != line[i]:
                newLine.append(c)
            else:
                processed = processInternalJunk(line[i])
                for j in processed:
                    newLine.append(correct(j))
            i+=1
        else:
            c=correct(line[i])
            newLine.append(c)
            i=i+1
    return newLine
"""
function: helper method to deal with special characters
input: string
"""
def correctChars(word):
    for i in chars:
        s = word.split(i)
        if word[len(word)-1] == ':':
            ls = []
            for j in s:
                c = correct(j)
                ls.append(c)
            word = i.join(ls) + ":"
        elif len(s) != 1:
            ls = []
            for j in s:
                c = correct(j)
                ls.append(c)
            word = i.join(ls)
    return word
"""
function: process a string with internal junk chars
"""
def processInternalJunk(word):
    lsWord = []
    startInd = 0
    for i in range(1, len(word)-1):
        if word[i] in specialChars or word[i] in numbers:
            lsWord.append(word[startInd:i])
            startInd=i+1
    return lsWord
"""
function: count the differences in files
args: files in two dimensional list form
"""
def diffCount(fileOne, fileTwo):
    diffCount = 0
    for i in range(0, len(fileOne)):
        for j in range(0, len(fileOne[i])):
            if fileOne[i] != fileTwo[i]:
                diffCount += 1
    return "Differences between the two files: " + str(diffCount)
"""
function: remove special chars
"""
def removeSpecialChars(line):
    for i in line:
        for j in i:
            if j in specialChars:
                j = ""
    return line
"""
function: determine if a string is a number
"""
def isNum(word):
    #check if word is a number
    if word[0] not in numbers or word[0] not in chars:
        return False
    i=1
    while isNum and i < len(word):
        if word[i] not in numbers:
            if i == len(word) - 1 and word[i] in chars:
                return True
            else:
                return False
        i=i+1
    return True
"""
function: determine if a string is a number with a different technique
"""
def isNumTwo(word):
    numCount=0
    letterCount=0
    for i in word:
        if i in numbers:
            numCount+=1
        if i in alphabet:
            letterCount+=1
    if letterCount > 0 or numCount == 0:
        return False
    else:
        return True
"""
function: determine if a string is junk
"""
def isJunkString(word):
    #look at backslash
    backCount=0
    if "\\" in r"%r" % word:
            return True
    else:
        return False
"""
function: determine if a string has internal junk chars
"""
def hasInternalJunk(word):
    for i in range(1, len(word)-1):
        if word[i] in specialChars or word[i] in numbers:
            return True
    return False
"""
function: determine if a string has internal special chars
"""
def hasSpecialChars(word):
    for i in word:
        if i in chars:
            return True
    return False
