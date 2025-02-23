#int counterFunctionCalls

def max3(x,y,z):
#{
    #int m
    global counterFunctionCalls
    counterFunctionCalls = counterFunctionCalls + 1
    if x>y and x>z:
        m = x
    elif y>x and y>z:
        m = y
    else:
        m = z
    return m
#}
      
#def main
#int i
counterFunctionCalls = 0

i = int(input())
print(i)

i = 1600
while i<=2000:
#{
    print(leap(i))
    i = i + 400
#}
