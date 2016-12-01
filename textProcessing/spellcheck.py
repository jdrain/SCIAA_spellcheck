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
numbers = ['0','1','2','3','4','5','6','7','8','9']
specialChars = '!@#$%^&*()_-+=?'
chars=['/',',',';','\'','.']

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
"""

"""
function: spellcheck the extracted data before compilation into final
file
list should be of the form: [[key1, val1, val2, ...,valn],...]
"""
def spellcheck_extracted_data(file_list):
    ls=[]
    for i in file_list:
        ls1=[i[0]]
        for j in range(1, len(i)):
            #leave numbers alone 
            #leave small words alone
            if len(i[j])<=2:
                ls1.append(i[j])
            elif is_num(i[j]):
                ls1.append(i[j])
            else:
                ls1.append(correct(i[j]))
        ls.append(ls1)
    return ls
"""
function: count the differences in files
args: files in two dimensional list form
"""
def diff_count(fileOne, fileTwo):
    diffCount = 0
    for i in range(0, len(fileOne)):
        for j in range(0, len(fileOne[i])):
            if fileOne[i] != fileTwo[i]:
                diffCount += 1
    return "Differences between the two files: " + str(diffCount)
"""
function: determine if a string is a number
"""
def is_num(word):
    #check if word is a number
    if word[0] not in numbers:
        return False
    if len(word)>1:
        i=1
        while i<len(word):
            if word[i] not in numbers:
                return False
            i+=1
    return True
