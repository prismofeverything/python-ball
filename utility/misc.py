import time

def timefunc(func, times=1):
    before = time.time()

    for x in range(times):
        func()

    after = time.time()

    return after - before
        





def frombyte(byte):
    power = len(byte) - 1
    char = 0

    for bit in byte:
        if bit == '1':
            char += 2 ** power

        power -= 1

    return chr(char)

def tobyte(char):
    number = ord(char)
    base = int(math.floor(math.log(number, 2)))
    byte = ''

    for power in range(base, -1, -1):
        binarydigit = 2 ** power
        if binarydigit <= number:
            number -= binarydigit
            byte += '1'
        else:
            byte += '0'

    return byte

def fromhex(hex):
    return chr(int(hex, 16))
        
def tohex(char):
    return "%X" % ord(char)

def frominversehex(hex):
    return chr(256 - int(hex, 16))

def toinversehex(char):
    return "%X" % (256 - ord(char))

def frombytes(op):
    def fromb(bytes):
        message = ''

        lobytes = bytes.split(' ')
        for sobits in lobytes:
            message += op(sobits)

        return message

    return fromb

def tobytes(op):
    def tob(message):
        lobytes = []

        for char in message:
            lobytes.append(op(char))

        return ' '.join(lobytes)

    return tob

def read(filename):
    mo = open(filename, 'r')
    text = mo.read()
    mo.close()
    
    return text

def write(filename, what):
    mo = open(filename, 'w')
    mo.write(what)
    mo.close()

def translatefile(filename, op):
    message = read(filename)
    encoded = op(message)
    write(filename, encoded)

