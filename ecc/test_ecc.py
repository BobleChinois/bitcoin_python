import pytest

from ecc.ecc import FieldElement, Point


def test_FieldElement_valid():

    a = FieldElement(6, 13)

    assert a.num == 6
    assert a.prime == 13

def test_error():

    with pytest.raises(ValueError):
        a = FieldElement(6, -13)
    with pytest.raises(ValueError):
        b = FieldElement(21, 17)
    with pytest.raises(ValueError):
        c = FieldElement(-5, 23)
    with pytest.raises(ValueError):
        d = FieldElement(None, None)

def test_ne():
    a = FieldElement(2, 31)
    b = FieldElement(2, 31)
    c = FieldElement(15, 31)
    assert a == b
    assert (a != c) == True
    assert (a != b) == False
    
def test_add():
    a = FieldElement(2, 31)
    b = FieldElement(15, 31)
    c = FieldElement(17, 31)
    d = FieldElement(21, 31)
    e = FieldElement(7, 31)
    assert (a + b) == c
    assert (c + d) == e
 
def test_sub():
    a = FieldElement(29, 31)
    b = FieldElement(4, 31)
    c = FieldElement(25, 31)
    d = FieldElement(15, 31)
    e = FieldElement(30, 31)
    f = FieldElement(16, 31)
    assert (a - b) == c
    assert (d - e) == f

def test_mul():
    a = FieldElement(24, 31)
    b = FieldElement(19, 31)
    c = FieldElement(22, 31)
    assert (a * b) == c

def test_pow():
    a = FieldElement(17, 31)
    b = FieldElement(15, 31)
    c = FieldElement(5, 31)
    d = FieldElement(18, 31)
    e = FieldElement(16, 31)
    assert a**3 == b
    assert c**5 * d == e

def test_div():
    a = FieldElement(3, 31)
    b = FieldElement(24, 31)
    c = FieldElement(4, 31)
    d = FieldElement(17, 31)
    e = FieldElement(29, 31)
    f = FieldElement(11, 31)
    g = FieldElement(13, 31)
    assert a / b == c
    assert d**-3 == e
    assert c**-4 * f == g
   
def test_Point_valid():
    a = Point(None, None, 5, 7)
    with pytest.raises(ValueError):
        b = Point(4, 6, 5, 7)
    c = Point(3, -7, 5, 7)

    assert a.x == None
    assert c.x == 3
    assert c.y == -7
    
def test_ne():
    a = Point(3, -7, 5, 7)
    b = Point(18, 77, 5, 7)
    assert a != b
    assert a == a

def test_add():
    a = Point(None, None, 5, 7)
    b = Point(2, 5, 5, 7)
    c = Point(2, -5, 5, 7)
    d = Point(-1, 0, 6, 7)
    e = Point(3, 7, 5, 7)
    f = Point(-1, -1, 5, 7)
    g = Point(18, 77, 5, 7)
    # self.a != other.a (or b)
    with pytest.raises(TypeError):
        print(a + d)
    # other.x is None
    assert b + a == b
    # self.x is None
    assert a + b == b
    # self.x == other.x, self.y != other.y
    assert b + c == a
    # self == other, y == 0
    assert e + f == c
    # self == other, y != 0
    assert f + f == g
