# import hash module
# file should be at the same level of directory
import hash

# global values
# assume file exists
filename = input('File containing transactions: ')
block = open(filename).read()
transaction_list = []
coin_list = []
sender_list = []
recipient_list = []


# split the block
transaction_list = block.split(';')
for transaction in transaction_list:
    spilited_transaction = transaction.split(',')
    coin_list.append(spilited_transaction[0])
    sender_list.append(spilited_transaction[1])
    recipient_list.append(spilited_transaction[2])

# print in a more user-frinedly format
for i in range(len(transaction_list)):
    print('{0} gave {1} coins to {2}.'.format(sender_list[i], coin_list[i], recipient_list[i]))

# get the hash difficulity
# assume only gets integer
hash_difficulity = int(input('Hash difficulty: '))
num_to_try = int(input('Number of hashes to try: '))
hash_str_start = hash_difficulity * '0'

# mine the Lawcoin block
for i in range(num_to_try):
    hash_str = block + str(i)
    hash_value = hash.md5_hash(hash_str)
    if hash_value.startswith(hash_str_start):
        print('Found hash {0} using nonce {1}.'.format(hash_value, i))
        break
else:
    print('No block mined.')


