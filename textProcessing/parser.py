#parser to extract pertinent information from raw text files

from fuzzywuzzy import fuzz
from recognize_dates import get_date

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
    ls=[]
    for key in keys.keys():
        for i in find_keys(keys[key]["InitKeys"],file_list,keys[key]["EndKeys"]):
            ls.append(i)
    for i in ls:
        print(i)
        print(file_list[i[1]:i[2]])
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
            if filtered_data[i+1][3]>best_ratio:
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
            if (keys[key]["NextLineField"][0]==False and keys[key]["CheckField"][0]==False and
                    keys[key]["MultiLineField"][0]==False):
                ls.append([key,
                " ".join(remove_new_lines(file_list[start:end]))])
            else:
                #is the field on the next line or multiple lines?
                if keys[key]["NextLineField"][0]==True or keys[key]["MultiLineField"][0]==True:
                    #ignore newline chars
                    ls.append([key," ".join(file_list[start:end])])
                #is the field a checked field?
                if keys[key]["CheckField"][0]==True:
                    #deal with checked fields
                    ls.append(process_checked_field(file_list,key,start,end))
        i+=1
    return remove_extra_chars(ls,keys,nums)
"""
function: translate the output of extract_data into DB enterable format
"""
def database_format(data,keys,encoding_keys,date_conversions):
    #do stuff for key translation
    ls=[]
    encod_keys=encoding_keys.keys()
    print("\nNow formatting for DB\n")
    for i in range(0,len(data)):
        top_key=data[i][0]
        db_key=keys[top_key]["FieldName"][0]
        info=data[i][1:len(data[i])]
        added=False

        #for debug
        print("\nTop Key: "+top_key)
        print("DB Key: "+db_key)
        print("Info: ")
        print(info)
        if info==[]:
            pass
        else:
            #deal with estimated site dimensions
            #maybe generalize this segment of code later
            #but for now it will do

            if top_key=="estimated site dimensions":
                esd_keys=keys[top_key]["FieldName"]
                for i in process_site_dimensions(info,esd_keys):
                    ls.append(i)
                added=True
            elif top_key=="date":
                date=get_date(info,date_conversions)
                if date[1]!=None:
                    date[1]=date[1]+" ADDED BY GET DATE METHOD"
                    ls.append(date)
                    added=True
            elif top_key=="archaeological investigation":
                ai_keys=keys[top_key]["FieldName"]
                ai_encoded=keys[top_key]["Encoded"]
                for i in process_archaeological_components(info,ai_keys,ai_encoded):
                    ls.append(i)
                added=True
            #eventually add a db_column var
            #do stuff to deal with multi-option fields
            elif len(keys[top_key]["FieldName"]) > 1:
                key=keys[top_key]
                #we have a multi-option field
                for i in choose_multi_option_field(info,key):
                    ls.append(i)
                added=True
            #do stuff for numerically encoded fields
            if db_key in encod_keys:
                #process that ish
                #this block really should be a separate method
                ls.append(process_encoded_fields(info,db_key,encoding_keys))
                added=True
            if added==False:
                ls.append([db_key," ".join(info)+"ADDED WITH TOP KEY "+str(top_key)])

    #remove new lines from the output
    for i in range(0,len(ls)):
        ls[i][1]=remove_new_lines_str(ls[i][1])

    return ls
"""
function: process site dimensions
"""
def process_site_dimensions(info,keys):
    #find pure numbers
    nums=['1','2','3','4','5','6','7','8','9','0']
    ls=[]
    k=0
    print("\nprocessing site dimensions: \n")
    info=info[0].split();
    print("\ninfo: \n")
    print(info)
    print("\nkeys: \n")
    print(keys)
    for i in info:
        #is it a pure number?
        if k<len(keys):
            is_num=True
            for j in i:
                if j not in nums:
                    is_num=False
            if is_num==True:
                ls.append([keys[k],i])
                print("\nappended: \n")
                print([keys[k],i])
                k+=1
        else:
            break
    return ls

"""
function: process encoding key fields
"""
def process_encoded_fields(info,db_key,encoding_keys):
    best_ratio=0
    best_key="none"
    for key in encoding_keys[db_key]:
        rat=fuzz.ratio(str(key),str(info[0]))
        if rat > best_ratio:
            best_ratio=rat
            best_key=key
    if best_ratio >= 80:
        info=[encoding_keys[db_key][best_key]]
    else:
        info=[""]
    return [db_key," ".join(info)]
"""
function: deal with archaeological components
"""
def process_archaeological_components(info,keys,encoded):
    ls = []
    for i in range(0,len(info)):
        #is info[i] an x? if so, check if the next two words match a known key
        if (i <= len(info)-2) and (info[i]=='x'):
            potential_key = info[i+1]+" "+info[i+2]
            #calculate the fuzz ratio of this and all the keys
            ls=[]
            best_rat = 0
            best_rat_ind = 0
            for j in range(0, len(encoded)):
                rat=fuzz.ratio(potential_key,encoded[j])
                if rat > best_rat:
                    best_rat = rat
                    best_rat_ind = j
            if best_rat > 75:
                #take that ish
                ls.append([encoded[best_rat_ind],"Y"])
    return ls
"""
function: divide a multi-option field into its corresponding field in the DB,
based upon which value it has
"""
def choose_multi_option_field(field_info,key):
    #which key does field info match?
    ls=[]
    for i in field_info:
        best_ratio=0
        best_match=""
        for j in range(0,len(key["Encoded"])):
            rat=fuzz.ratio(str(key["Encoded"][j]),str(i))
            if rat>best_ratio:
                best_ratio=rat
                best_match=key["FieldName"][j]
        if best_ratio>=80:
            ls.append([best_match,"Y"])
        else:
            pass
    return ls

"""
function: deal with checked fields
"""
def process_checked_field(file_list,key,start,end):
    ls1=[]
    ls1.append(key)
    for j in range(start,end):
        if (j!=0 and len(file_list[j])==1 and
        file_list[j] != "\n" and len(file_list[j-1])!=1):
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
        if keys[key]["IsNonNumeric"][0]==True:
            #process out numeric data
            for j in range(1,len(ls[i])):
                for num in nums:
                    ls[i][j]=str(ls[i][j]).replace(num,"")
        elif keys[key]["IsNumeric"][0]==True:
            #process out non-numeric data
            for j in range(1,len(ls[i])):
                for char in ls[i][j]:
                    if char not in nums:
                        ls[i][j]=ls[i][j].replace(char,"")
    return ls
"""
function: remove new line chars from a list
"""
def remove_new_lines(file_list):
    for i in range(0, len(file_list)):
        file_list[i]=file_list[i].replace("\n","")
        file_list[i]=file_list[i].replace("\r","")
    return file_list
"""
function: remove new line chars from a string
"""
def remove_new_lines_str(s):
    s=s.replace("\n","")
    s=s.replace("\r","")
    return s
"""
function: remove underlines from the files
"""
def remove_underlines(file_list):
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
    ls=[]
    #for debug
    print(file_list)
    #take out nums after newline
    for i in range(1, len(file_list)):
        if (file_list[i] in nums and file_list[i-1]=="\n"):
            #don't add the newline num
            pass
        else:
            ls.append(file_list[i])
    return ls
