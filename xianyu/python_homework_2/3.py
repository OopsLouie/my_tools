loan_and_year = input('Enter total LOAN and YEAR seperated by comma:')

try:
    loan, year = loan_and_year.split(',')
    loan = int(loan)
    year = int(year)
except:
    print('invalid input')
    exit(0)

loan_type = input('Enter loan Mode:')

try:
    if loan_type.upper() == 'C':
        if year == 1:
            P = 6
        elif year <= 3:
            P = 6.15
        elif year <= 5:
            P = 6.40
        else:
            P = 6.55
    elif loan_type.upper() == 'G':
        if year <= 5:
            P = 4
        else:
            P = 4.5
    else:
        exit(0)
except:
    print('invalid input')


N = year * 12
R = P/12/100

M = loan * 10000 * R * ((1+R) ** N) / (((1+R) ** N) - 1)

print(int(M))





