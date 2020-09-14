grade = input('Please input grade:')


try:
    grade = int(grade)
except:
    print('invald input')

if grade > 80:
    print('A')
elif grade > 60:
    print('B')
elif grade > 40:
    print('C')
elif grade > 20:
    print('D')
else:
    print('E')
