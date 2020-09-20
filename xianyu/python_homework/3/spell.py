# constant
ALPHABET = "abcdefghijklmnopqrstuvwxyz"
# get input file and word list file
input_file = input("Input file: ")
word_list_file = input("Word list file: ")

# read file
words = open(input_file).read().split("\n")
standard_words_list = open(word_list_file).read().split("\n")
standard_words = {}
for standard_word in standard_words_list:
    standard_words[standard_word] = True

correction_cache = {}

# check spell
for word in words:
    potential_word_list = []
    if word not in standard_words:
        if word in correction_cache:
            print(word + "* -> " + correction_cache[word])
            continue
        # insert one more letter
        if len(word) != 1:
            for i in range(len(word)):
                potential_word = word[:i] + word[i+1:]
                if potential_word in standard_words:
                    potential_word_list.append(potential_word)
        # swap two consecutive letters
        if len(word) != 1:
            for i in range(len(word) - 1):
                potential_word = word[:i] + word[i+1] + word[i] + word[i+2:]
                if potential_word in standard_words:
                    potential_word_list.append(potential_word)
        # mistype a single letter
        for i in range(len(word)):
            for letter in ALPHABET:
                if word[i] == letter:
                    continue
                potential_word = word[:i] + letter + word[i+1:]
                if potential_word in standard_words:
                    potential_word_list.append(potential_word)
        if potential_word_list:
            print(word + " -> " + ", ".join(potential_word_list))
        else:
            print(word + " -> (No suggestions)")
        correction_cache[word] = ", ".join(potential_word_list)


