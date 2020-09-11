# import hash module
# file should be at the same level of directory
import hash

# global values
# assume input filename will always be right because we cannot use while-loop in task
filename = input('Word file: ')
# assume target word is not empty
target_word = input('Collisions for: ')
# where to save result
collision_word_list = []
# final results
sorted_collision_word_list = []

# open file and read from it
word_list = open(filename).read().split('\n')

# search for collision
target_hash_result = hash.short_hash(target_word)
for word in word_list:
    if hash.short_hash(word) == target_hash_result:
        collision_word_list.append(word)

# sort collision_word_list by first character
collision_word_list.sort()

# output
for collision_word in collision_word_list:
    print(collision_word)
if len(collision_word_list) == 0:
    print('No Collisions found')
