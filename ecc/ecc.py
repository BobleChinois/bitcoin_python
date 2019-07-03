# Elliptic Curves library for cryptography

class FieldElement:

    def __init__(self, num, prime):
        # What happens when we create an object of this class
        if  num >= prime or num < 0: # Use try/except instead of if?
            error = f'{num} not in field range 0 to {prime - 1}'
            raise ValueError(error)
        self.num = num # you need this to define your object attributes according to the inputs of the function
        self.prime = prime

    def __repr__(self):
        # this overwrite the standard print() function
        return f'FieldElement {self.prime}({self.num})'

    def __eq__(self, other):
        # this overwrite the standard == operator
        if other is None:
            return False # return an error instead of simply False?
        # you need two things to compare, if not it should fail
        return self.num == other.num and self.prime == other.prime
