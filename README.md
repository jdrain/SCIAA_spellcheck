# SCIAA_spellcheck
This repository holds files for a spell checker

![alt-text](https://travis-ci.org/jdrain/SCIAA_spellcheck.svg?branch=master)

1. Improvements Needed
  + support fields that are multiple lines
  + support fields that are circled
  + support fields that are on the next line from the field name 
  + spellcheck just needs to be better in general. Although it may be
    close to the point of diminishing returns...
2. Usage
  + spellcheck.py holds methods to run a spellchecker on a file
  + parser.py parses a file to grab pertinent info
  + checkAndParse.py implements these to process a textfile from I to O.
implementing these methods
  + other files are scripts to test these methods
  + a few .json files are included; these hold information that the
    parser needs to decide which lines to pull and which to ignore.
  + output can be formatted as .txt or .csv, depending on
    preference
