#!/bin/zsh
#spellchecks processed text files and then parses them
#takes one command line arg which is a directory containing text files

for i in ls $1; do python ../SCIAA_spellcheck/checkAndParse.py $i >> checkAndParseTest.txt; done;
