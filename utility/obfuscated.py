def frombytes(b):
    m = ''

    l = b.split(' ')
    for s in l:
        p = 7
        c = 0

        for i in s:
            if i == '1':
                c += 2 ** p

            p -= 1

        m += chr(c)

    return m


def tobytes(m):
    l = []

    for c in m:
        n = ord(c)
        s = ''

        for p in range(7, -1, -1):
            g = 2 ** p
            if g <= n:
                n -= g
                s += '1'
            else:
                s += '0'

        l.append(s)

    return ' '.join(l)
