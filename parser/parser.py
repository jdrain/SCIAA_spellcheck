#parser to extract pertinent information from raw text files

"""
We need:
    -a function to recognize key expressions
    -a list of the key expressions
"""

keys=["descriptive site type (see handbook):", "prehistoric", "historic",
      "archaeological investigation (circle):", "level of significance "
      "(circle):", "justification:", "landform location:", "site "
      "elevation (above msl):", "On site soil type:", "soil "
      "classification:", "major river system (circle):", "nearest "
      "river/stream:", "estimated site dimensions:", "site depth:",
      "cultural features (type and number):", "general site "
      "description:"]
keys.sort() #alphabetize list

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
            fileList.append(line)
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


