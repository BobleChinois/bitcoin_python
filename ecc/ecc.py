# Elliptic Curves library for cryptography

class FieldElement:

    def __init__(self, num, prime):
        # What happens when we create an object of this class
        if num == None or prime == None:
            error = f'None value not allowed'
            raise ValueError(error)
        if  num >= prime or num < 0: # Use try/except instead of if?
            error = f'{num} not in field range 0 to {prime - 1}'
            raise ValueError(error)
        self.num = num # you need this to define your object attributes according to the inputs of the function
        self.prime = prime

    def __repr__(self):
        # this overwrite the standard `print()` function
        return f'FieldElement {self.prime}({self.num})'

    def __eq__(self, other):
        # this overwrite the standard `==` operator
        if other is None:
            return False # return an error instead of simply False?
        # you need two things to compare, if not it should fail
        return self.num == other.num and self.prime == other.prime

    def __ne__(self, other):
        # this overwrite the standard `!=` operator
        return not (self == other)
    
    def __add__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot add two numbers in different Fields')
        num = (self.num + other.num) % self.prime
        return self.__class__(num, self.prime) # return self.__class__ means retur a new object of the same class

    def __sub__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot substract two numbers in different Fields')
        num = (self.num - other.num) % self.prime
        return self.__class__(num, self.prime)  

    def __mul__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot multiply two numbers in different Fields')
        num = (self.num * other.num) % self.prime
        return self.__class__(num, self.prime)  

    def __pow__(self, exponent):
        n = exponent % (self.prime - 1)
        num = pow(self.num, n, self.prime)
        return self.__class__(num, self.prime)

    def __truediv__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot divide two numbers in different Fields')
        num = self.num * pow(other.num, (self.prime-2), self.prime) % self.prime
        return self.__class__(num, self.prime)

class Point:

    def __init__(self, x, y, a, b):
        if x is None and y is None:
            return #Isn't there a better way?
        if y**2 != x**3 + a * x + b:
            raise ValueError(f'({x}, {y}) is not on the curve')
        self.a = a
        self.b = b
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y \
                and self.a == other.a and self.b == other.b

    def __ne__(self, other):
        return not (self == other)

    def __repr__(self):
        if self.x is None:
            return 'Point(infinity)'
        else:
            return f'Point({self.x}, {self.y})_{self.a}_{self.b}'

    def __add__(self, other):
        if self.a != other.a or self.b != other.b:
            raise TypeError(f'Points {self}, {other} are not on the same curve')

        if self.x is None:
            return other
        if other.x is None:
            return self

        if self.x == other.x and self.y != other.y:
            return self.__class__(None, None, a, b)

        if self == other and self.y == 0:
            return self.__class__(None, None, a, b)

        if self.x != other.x and self.y != other.y:
            m = (self.y - other.y)/(self.x - other.x)
            x = pow(m, 2) - self.x - other.x
            y = self.y + m*(x - self.x)
            return self.__class__(x, y, a, b)

        if self.x == other.x and self.y == other.y:
            m = (3*pow(self.x, 2) + a) / (2 * self.y)
            x = pow(m, 2) - self.x - other.x
            y = self.y + m*(x - self.x)
            return self.__class__(x, y, a, b)
