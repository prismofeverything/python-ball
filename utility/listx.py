def reverse(l):
    l.reverse()
    return l

def flatten(l, types=(list,tuple)):
    i = 0

    while i < len(l):
        while isinstance(l[i], types):
            if not l[i]:
                l.pop(i)
                if not len(l):
                    break
            else:
                l[i:i+1] = list(l[i])

        i += 1

    return l

