import math

r = input('Please enter radium: ')

try:
    r = int(r)
    volume = 4 * (r**3) * math.pi / 3
    superficial = 4 * (r**2) * math.pi
    print('Volume is %f' %(volume))
    print('Superficial is %f' %(superficial))
except:
    print('invalid input')
