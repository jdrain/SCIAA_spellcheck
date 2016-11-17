#parser to extract pertinent information from raw text files

from fuzzywuzzy import fuzz

"""
TODO:
    -Fix the recognition of 'excavation' as 'elevation
    -How do we cope with noise in these checkmark fields?
    -Remove the underline characters
"""

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
    return choose_best(ls)
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
            rat=fuzz.ratio(str(" ".join(file_list[i:j])),str(" ".join(key)))
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
function: choose the best extraction for each key
"""
def choose_best(filtered_data):
    data=[]
    i=0
    while i<len(filtered_data):
        best_ratio=filtered_data[i][3]
        best_ratio_ind=i
        while i<len(filtered_data)-1 and filtered_data[i][0]==filtered_data[i+1][0]:
            print("entered while loop")
            if filtered_data[i+1][3]>best_ratio:
                print("new best ratio")
                best_ratio=filtered_data[i+1][3]
                best_ratio_ind=i+1
            i+=1
        data.append(filtered_data[best_ratio_ind])
        i+=1
    return data
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
function: deal with circled fields
"""
def process_circled_field(file_list,key,start,end):
    ls=[]
    ls.append(key)
    for i in range(start+1,end-1):
        print("element "+str(i)+": "+str(file_list[i]))
        if (len(file_list[i])!=1 and len(file_list[i-1])==1
                and len(file_list[i+1])==1):
            print("found a circled option")
            ls.append(file_list[i])
    return ls
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
function: remove underlines from the files
"""
def remove_underlines(file_list):
    nums=['1','2','3','4','5','6','7','8','9','0']
    ls=[]
    i=0
    while i<len(file_list):
        file_list[i]=file_list[i].replace("_"," ")
        file_list[i]=file_list[i].replace("-"," ")
        file_list[i]=file_list[i].replace("."," ")
        ls.append(file_list[i])
        i+=1
    return ls
"""
function: remove the numbers from the beginnings of lines
"""
def remove_newline_nums(file_list):
    nums=['1','2','3','4','5','6','7','8','9','0']
    nums2=[i+" " for i in nums]
    ls=[]
    #for debug
    print(file_list)
    #take out nums after newline
    for i in range(0, len(file_list)):
        if (i>0 and file_list[i] in nums or (file_list[i]) in nums2
                and file_list[i-1]=="\n"):
            #don't add the newline num
            pass
        else:
            ls.append(file_list[i])
    return ls
