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
