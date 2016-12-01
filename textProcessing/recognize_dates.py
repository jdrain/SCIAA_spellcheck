from textProcessing import processData.processJSON as processJSON
from fuzzywuzzy import fuzz.ratio as ratio

"""
Function: take in a file (slit over white space) and then extract a date
from it
"""

def get_date(input_file, date_conversions):
    conversions=processJSON(date_conversions)
    date_chars=['1','2','3','4','5','6','7','8','9','/']
    for i in range(0,len(input file)):
        #two cases, (i) if it is all together "MM/DD/YYYY", we can just take,
        #but if it is separated (ii) "Month DD/YYYY" need to be attentive
        if ratio(input_file[i],"date")>=80:
            #found the date, probably
            correct_format=True
            for j in input_file[i+1]:
                if j not in date_chars:
                    correct_format=False
                    break
            if correct_format==True:
                #cool, pump this puppy outta here
                date=input_file[i+1]
                break
            else:
                #shit, gotta do more work
                for j in conversion.keys():
                    if ratio(j,input_file[i+1])>=80:
                        #found a month
                        month=conversion[j]
                        break
                date=month+input_file[i+2]
                break
    return date

