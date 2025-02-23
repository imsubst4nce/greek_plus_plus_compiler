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


def fib(x):
#{
    global counterFunctionCalls
    counterFunctionCalls = counterFunctionCalls + 1
    if x<0:
        return -1
    elif x==0 or x==1:
        return 1
    else:
        return fib(x-1)+fib(x-2)
#}
     
     
def isPrime(x):
#{
    #int i

    def divides(x,y):
    #{
        global counterFunctionCalls
        counterFunctionCalls = counterFunctionCalls + 1
        if y == (y//x)*x:
            return 1
        else:
            return 0
    #}

    global counterFunctionCalls
    counterFunctionCalls = counterFunctionCalls + 1
    i = 2
    while i < x:
    #{
        if divides(i,x) == 1:
            return 0
        i = i + 1
    #}
    return 1
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
print(leap(2023))
print(leap(2024))
print(quad(3))
print(fib(5))

i=1
while i<=12:
#{
    print(isPrime(i))
    i = i + 1
#}

print(counterFunctionCalls)

