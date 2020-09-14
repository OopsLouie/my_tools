gender = input('Please enter your gender(M or F):')
age = input('Please enter your age:')
try:
    if gender.upper() == 'M':
        if int(age) >= 22:
            print('can get marriaged')
        else:
            print('can not get marriaged')
    elif gender.upper() == 'F':
        if int(age) >= 20:
            print('can get marriaged')
        else:
            print('can not get marriaged')
    else:
        print('invalid input')
except:
    print('invalid input')



