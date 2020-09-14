from random import random
from math import sqrt

times = 1000000
hits = 0
for i in range(1,times):
    x,y = random(),random()
    dist = sqrt(x**2 + y**2)
    if dist <=1.0:
        hits = hits + 1
    pi = 4*(hits/times)
print('pi is %.2f' % pi)
