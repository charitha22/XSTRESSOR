from z3 import *


x = Int('x')
y = Int('y')
z = Int('z')

arr = [x, y , z]

#x = y + 1

for i in range(0, len(arr)-1):
#     x = y +1
     arr[i] = arr[i+1] 

print(arr)

solve(arr[0]>0, arr[1]>0, arr[2]>0)