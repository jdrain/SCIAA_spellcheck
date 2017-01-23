from  processData import processJSON
import json
import sys

"""
Script to reformat JSON data into a more explicit scheme. Doubt there will
be much use for this beyond what I'm writing it for

arg1: input JSON
arg2: output JSON
"""

def parse_json(json_in, json_out, new_keys):

    old_json = processJSON(json_in)

    new_dict = {}
    for form_key in old_json.keys():
        if form_key != "DateConversions":
            form_dict = {}
            for field_key in old_json[form_key].keys():
                i = 0
                field_dict = {}
                while (i < len(old_json[form_key][field_key])):
                    field_dict[new_keys[i]] = old_json[form_key][field_key][i]
                    i += 1
                form_dict[field_key] = field_dict
            new_dict[form_key] = form_dict

    #write out to the new JSON
    print(new_dict)
    with open(json_out, 'w') as out:
        json.dump(new_dict, out, sort_keys = True, indent = 4, ensure_ascii = False)

if __name__ == "__main__":

    #new key values that will give us a more explicit naming system for the JSON
    new_key_ls = [
            "InitKeys",
            "EndKeys",
            "NextlineField",
            "CheckField",
            "MultiLineField",
            "IsNumeric",
            "IsNonNumeric",
            "FieldName",
            "Encoded"
            ]

    #parse the JSON
    parse_json(sys.argv[1], sys.argv[2], new_key_ls)
