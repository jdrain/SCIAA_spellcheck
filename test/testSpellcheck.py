#test script for spellcheck
import spellcheck

#read in the file
f = spellcheck.readFile("textFiles/binarized_smaller_printed_files38AL0111_68-1-1_Revisit_1a.pdf.tiff.png.txt")

print("\noriginal file:\n")
for i in range(0, len(f)):
    print(f[i])

#correct the file
cf = spellcheck.correctFile(f)

print("\nfile corrected with technique one:\n")
for i in range(0, len(cf)):
    print(cf[i])

#print the differences between the two files
print(spellcheck.diffCount(f, cf))
