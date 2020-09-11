# import hash module
# file should be at the same level of directory
import hash

# global values
# assume hash str is valid
hash_to_break = input('Hash to break: ')
# assume dictionary file exist
dictionary_file = input('Dictionary file: ')
# password list
password_list = open(dictionary_file).read().split('\n')

for password in password_list:
    # cal hash for original password
    if hash.md5_hash(password) == hash_to_break:
        print(password)
        break
    # cal hash for transformed password
    transformed_password = password.replace('a', '@').replace('A', '@').replace('e', '3').replace('E', '3').replace('i', '1').replace('I', '1').replace('o', '0').replace('O', '0')
    if transformed_password == password:
        continue
    else:
        if hash.md5_hash(transformed_password) == hash_to_break:
            print(transformed_password)
            break
else:
    print('No password found')

