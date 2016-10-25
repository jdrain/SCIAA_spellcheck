"""
data will come in as a list
"""

"""
function: compile list of form [['key', ['word1', 'word2']],...]
down to [['key word1 word2]]
"""
def compileList(data):
    simple_ls = []
    for i in data:
        s ="\n"+i[0]+"\n"+" ".join(i[1])+"\n"
        simple_ls.append(s)
    return simple_ls


"""
function: write the list back to a text file
"""
def toText(path, data):
    f=open(path, 'w')
    for i in data:
        f.write(i)
    f.close()
