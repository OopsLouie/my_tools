### Filename: clean.py
### Author: Your name here.
### Reads a file containing arbitrary text. Sanitzes the input text, removing
### all punctuation and converting words to lowercase. Writes those words to
### another text file in order with one word per line.

# DO NOT MODIFY THIS LINE. Imports a library to check whether a file exists.
import os

# All of the punctuation characters that should be removed during data cleaning.
PUNCTUATION = ',!.?;"()-\\:\'' 

# TODO: Request as input the names of two files: the input text and the
# file to which the cleaned words should be written. Store the input
# filename in the variable "input_filename" and the output filename in
# the variable "output_filename"
input_filename = input("Input file: ")
output_filename = input("Output file: ")

# DO NOT MODIFY THIS LINE. Retrieve the words from the specified file.
text = open(input_filename).read()

# TODO: The variable "text" contains the contents of the input file
# as a string. Clean this text and produce a list of strings containing
# the cleaned words from the text. Save this list of strings to the variable
# "words".

text_clean = text
# remove punctuation
for punctuation in PUNCTUATION:
    text_clean = text_clean.replace(punctuation, "")

# replace "\n" & "\t" with " "
text_clean = text_clean.replace("\n", " ")
text_clean = text_clean.replace("\t", " ")

# convert text_clean to lowercase
text_clean = text_clean.lower()

# break text_clean into lists of words
words = text_clean.split(" ")

# remove whitespace
index = 0
while index < len(words):
    if not words[index]:
        del words[index]
    else:
        index += 1

# remove words do not consist solely of letters
index = 0
while index < len(words):
    if not words[index].isalpha():
        del words[index]
    else:
        index += 1

# DO NOT MODIFY ANYTHING BELOW THIS POINT.
# Writes each item in "words" (a list of strings) to a text file whose name is
# stored in "output_filename", one word per line. Print an error message if
# the file already exists.
if os.path.exists(output_filename):
    print("ERROR: file {0} already exists. Quitting without saving.".format(output_filename))
else:
    fp = open(output_filename, 'w')
    fp.write('\n'.join(words))
    fp.close()

