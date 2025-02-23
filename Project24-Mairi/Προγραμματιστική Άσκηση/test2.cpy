#int counterFunctionCalls
def max3(x,y,z):
#{
    #int m 
    ## comment comment ##
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
     
def isPrime(x):
#{
    #int i

    def divides(x,y):
    #{
        ## comment comment##
        global counterFunctionCalls
        counterFunctionCalls = counterFunctionCalls + 1 
        if y == (y//x)*x:
            return 1
        else :
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

## comment comment ##

i = int(input())
print(i)

print(max3(5,2,1))

i=1
while i<=12:
#{
    print(isPrime(i))
    i = i + 1
#}

print(counterFunctionCalls)