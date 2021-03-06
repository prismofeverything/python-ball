import math

def gcd(a, b):
    if b == 0: return a
    else: return gcd(b, a % b)

def roundTo(base, unit):
    over = base % unit
    gap = unit - over

    if gap <= unit / 2:
        return base + gap
    else:
        return base - over

def listand(l, p):
    if l == []: return True
    elif not p(l[0]): return False
    else: return listand(l[1:], p)

def listor(l, p):
    if l == []: return False
    elif p(l[0]): return True
    else: return listor(l[1:], p)

def makeIsFactor(n):
    def isf(x):
        return n % x == 0

    return isf

def makePrimes():
    at = 2
    primes = [2]
    
    while True:
        yield at
        
        found = 0
        while not found:
            at += 1
            isfactor = makeIsFactor(at)
            
            found = not listor(primes, isfactor)
            
        primes.append(at)

def factor(n):
    factors = [x for x in range(1, math.ceil(math.sqrt(n))) if n % x == 0]
    factors.extend([n / y for y in factors])
    factors.sort()

    return factors

def uniqueFactorization(n):
    if n == 0: return [0]
    if n == 1: return [1]

    def unifac(n, factors, prime, primes):
        if prime == n:
            factors.append(n)
            return factors
        elif n % prime == 0:
            factors.append(prime)
            return unifac(n / prime, factors, prime, primes)
        else:
            return unifac(n, factors, primes.next(), primes)

    primes = makePrimes()
    return unifac(n, [], primes.next(), primes)

def uf(n): return uniqueFactorization(n)
    

def baseList(rep, base):
    maxPower = int(math.ceil(math.log(rep, base)))
    scale = base ** maxPower

    if not rep == scale:
        maxPower -= 1

    rule = [0 for x in range(maxPower + 1)]

    for power in range(maxPower, -1, -1):
        scale = base ** power

        while rep >= scale:
            rep -= scale
            rule[power] += 1

    return rule

def digitsToString(digits):
    def toString(string, digit):
        return str(digit) + str(string)

    return reduce(toString, digits)

def baseString(rep, base):
    translat = baseList(rep, base)
    return digitsToString(translat)










class Ratio:
    def __init__(self, over, under):
        self.over = over
        self.under = under

        self.simplify()

    def __repr__(self):
        return "" + str(self.over)[:5] + ":" + str(self.under)[:5]
        
    def __cmp__(self, other):
        return cmp(self.value(), other.value())

    def __getitem__(self, index):
        return self.rep()[index]

    def __add__(self, other):
        under = self.under * other.under
        first = self.under * other.over
        second = other.under * self.over

        return Ratio(first + second, under)

    def __sub__(self, other):
        return self + other.negative()

    def __mul__(self, other):
        over = self.over * other.over
        under = self.under * other.under

        return Ratio(over, under)

    def __div__(self, other):
        return self * other.inverse()

    def clone(self):
        return Ratio(self.over, self.under)

    def value(self):
        return float(self.over) / self.under

    def rep(self):
        return (self.over, self.under)

    def simplify(self):
        common = gcd(self.over, self.under)
        if common > 1:
            self.over /= common
            self.under /= common

        return self

    def normalize(self):
        while self.value() >= 2.0:
            self.under *= 2
        while self.value() < 1.0:
            self.over *= 2

        return self.simplify()

    def invert(self):
        between = self.over
        self.over = self.under
        self.under = between

        return self

    def negative(self):
        return Ratio(-self.over, self.under)

    def inverse(self):
        return Ratio(self.under, self.over)

    def between(self, other):
        if self > other:
            return self * other.inverse()
        else:
            return other * self.inverse()















# thought experiment, probably not usable

class Primes:
    def __init__(self):
        self.primes_seen = []
    def lastPrime(self):
        if len(self.primes_seen) > 0:
            return self.primes_seen[len(self.primes_seen) - 1]
        else:
            return 1
    def nextPrime(self):
        not_found = 1
        seek = self.lastPrime()

        while not_found:
            seek += 1
            possibly_prime = 1
            seen = 0

            while possibly_prime and seen < len(self.primes_seen):
                prime = self.primes_seen[seen]

                if seek % prime == 0:
                    possibly_prime = 0
                else:
                    seen += 1

            if possibly_prime:
                self.primes_seen.append(seek)
                not_found = 0

        return seek

def gcdFromPrimes(a, b):
    primes = Primes()
    common = 1
    not_found = 1

    while not_found:
        prime = primes.nextPrime()

        if prime > a or prime > b:
            not_found = 0
        else:
            while a % prime == 0 and b % prime == 0:
                a /= prime
                b /= prime
                
                common *= prime

    return common

