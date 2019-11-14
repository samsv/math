from functools import reduce


def abs(a): return a if a > 0 else -a


def mod(a,b):
    a = abs(a)
    while a > 0:
        a -= b
    return 0 if a == 0 else a + b


def mul(a, b):
    """
    Multiplies two numbers
    """

    def pe_notation(x):
        """
        Transform x such that
        x = m * 10 ** n with
        "m" being an integer
        """
        m, n = float(x), 0
        m_str = str(m)
        while len(m_str) != m_str.find('.') + 1:
            if (m_str.find("e") != -1):
                m, n = m_str.split("e")
                n = int(n)
                dot = m.find(".")
                if (dot+1):
                    m = m[0:dot]+m[dot+1:]
                    n -= len(m[dot:])
                break
            dot = m_str.find(".")
            m_str = m_str[:dot] + m_str[dot+1:dot+2] + "." + m_str[dot+2:]
            m = float(m_str)
            n -= 1
        return int(m), n

    def longmult(a, b):
        """
        Performs long multiplication on x, y
        """
        def mult(a, b):
            """
            Multiplies two integers
            """
            acc = 0
            M = max(abs(b),abs(a))
            m = min(abs(b),abs(a))
            for _ in range(abs(m)):
                acc = acc + M
            
            return - acc if b < 0 else acc

        def mult10(a): return (a << 3) + (a << 1)

        def correct_base(m, n):
            """
            Given an integer in scientific notation (mantissa(m), exponent(n)) returns
            the multiplication m * 10 ** n
            """
            return m if n == 0 else correct_base(mult10(m), n-1) 

        a_str = str(abs(a))

        p = sum([
                correct_base(mult(int(a_str[-(i+1)]), b), i) 
                for i in range(len(a_str))]
            )
        
        return -p if a < 0 else p
        
    if type(a) == int and type(b) == int:
        return longmult(a, b)

    m_a, n_a = pe_notation(a)
    m_b, n_b = pe_notation(b)
    m = longmult(m_a, m_b)
    n = n_a + n_b
    return float(str(m) + "e" + str(n)) # converts from scientific notation to float


def divide(a, b):
    if b == 0: raise ZeroDivisionError
    return mul(a, inverse(b))


def inverse(a):
    """
    Computes 1/a
    """
    tol = 1e-10
    x = float("0." + "0" * len(str(a)) + "1")
    err = 1
    while abs(err) > tol: 
        x = mul(x, 2 - mul(a,x))
        err = 1 - mul(a,x)
    return x


def ln(x):
    m, n = sci_notation(x)
    k = 1 / (m - 1)
    k = 2 * k + 1
    return mul(2, sum([divide(1,(mul(i,pow(k, i)))) for i in range(1, 50, 2)])) + \
            mul(n, 2.3025851)


def pow(x, y):
    if y == 0: return 1

    def pow_int(x, integer):
        return 1 if integer == 0 else x * pow_int(x , integer-1)

    if type(x) == type(y) and type(x) == int:
        return pow_int(max(x, y), min(x, y))

    if type(x) == int:
        return pow_int(y, x)

    if type(y) == int:
        return pow_int(x, y)


def exp(x):
    return sum([divide(pow(x, k), fact(k)) for k in range(1,100)]) + 1


def fact(x):
    return reduce(lambda x,y:x*y, range(x+1), 1) + 1


def sci_notation(x):
    """
    Transform x into the scientific notation
    returns "m" and "n" such that
    x = m * 10 ** n.
    """
    x = float(x)
    x_str = str(x)
    n = 0

    if x_str.find("e") != -1:
        m, n = x_str.split("e")
        return float(m), int(n)
    
    m_str, n_str = x_str.split(".")
    m, n = int(m_str), 0
    
    while len(m_str) != 1 or m_str == "0":
        if abs(m) == 0:
            m_str = n_str[0]
            n_str = n_str[1:]
            n -= 1
        else:
            n_str = m_str[-1] + n_str
            m_str = m_str[:-1]
            n += 1
    
    m = float(m_str + "." + n_str) if x > 0 else -float(m_str + "." + n_str)
    return m, n


x, y = 342, 0.5

from math import log
import math

print(math.exp(x))
print(exp(x))
print(math.exp(y))
print(exp(y))

# x = 100
# print(log(x))
# print(ln(x))

# print(log(x), log(y))
# print(ln(x), ln(y))
