from lxml import etree, objectify

"""
Module to take a dictionary and turn it into an XML element
"""

xml='''<?xml version="1.0" encoding="UTF-8"?>
    <Tests>
        </Tests>
            '''
root = objectify.fromstring(xml)

def create_object(data, header):
    """
    create an XML element
    """
    element = objectify.Element(header)
    for i in data:
        element.set(i[0], i[1])
    return element

def print_object(XML_object):
    root.append(XML_object)
    objStr = etree.tostring(root,pretty_print=True,xml_declaration=True)
    print(objStr)

