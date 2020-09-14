n = input('Please input n:')
m = input('Please input m:')

n = int(n)
m = int(m)

sum = 0
height = n

while m:
    sum += height
    height = height / 4
    sum += height
    m -= 1
sum -= height

print('%.2f' % sum)
print('%.2f' % height)
