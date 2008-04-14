def mor(l, conditions):
    for c in conditions:
        if c(l):
            return true

    return false

def mand(l, conditions):
    for c in conditions:
        if not c(l):
            return false

    return true

def filterlist(ls, conditions):
    [l for l in ls if lor(l, conditions)]

