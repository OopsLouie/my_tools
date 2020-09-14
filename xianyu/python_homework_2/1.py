temp_str = input('What is the temperature?')

try:
    if temp_str[-1].upper() == 'F':
        print('The converted temperature is %dC' % (int((float(temp_str[:-1]) - 32) / 1.8)))
    elif temp_str[-1].upper() == 'C':
        print('The converted temperature is %dF' % (int((float(temp_str[:-1]) * 1.8 + 32))))
    else:
        print('invalid input')
except:
    print('invalid input')
