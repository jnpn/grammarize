'''prelude: basic functional functions'''

def identity(v):
    return v

def flatten(l):
    r = []
    for e in l:
        if type(e) is not list:
            r.append(e)
        else:
            r.extend(flatten(e))
    return r

# flatten([])      -> []
# flatten([1])     -> [1]
# flatten([1 2])   -> [1 2]
# flatten([[1]])   -> [1]
# flatten([[1] 2]) -> [1 2]
# flatten([1 [2]]) -> [1 2]

def isnt(x):
    return lambda y: y is not x

def take(g,n):
    return [next(g) for i in range(n)]

def shuffler(a):
    n = len(a)
    while True:
        yield a[math.floor(random()*n-1)]
