def trivial(a, b):
    i, j, k, occors = 0,0,0,0
    m = len(a)
    n = len(b)
    for k in range(n):
        i = m-1
        j = k
        while (i >= 0 and a[i] == b[j]):
            i -= 1
            j -= 1
            if (i < 0): 
                occors += 1
    return occors
    
    
print trivial("casa", "minha casa e casa de casaco")