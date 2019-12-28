def rising_edge(eval, a, b):
    m = (a+b)//2
    if a > b:
        return -1
    if eval(m):
        if m == a:
            return a
        else:
            lower = rising_edge(eval, a, m-1)
            if lower == -1:
                return m
            else:
                return lower
    else:
        return rising_edge(eval, m+1, b)

def falling_edge(eval, a, b):
    def inverse(i):
        return not eval(i)
    return rising_edge(inverse, a, b)
