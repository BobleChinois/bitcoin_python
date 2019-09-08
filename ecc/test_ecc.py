import pytest

from ecc.ecc import FieldElement, Point, S256Field, S256Point, G, N, A, B

@pytest.fixture
def fieldelement():
    valid = [(6, 13), (29, 31), (2, 31), (15, 31), (17, 31), (21, 31), (7, 31)] 
    invalid = [(6, -13), (21, 17), (-5, 23), (None, None)] 

    return [valid, invalid]

def test_invalid(fieldelement):

    elements = fieldelement[1]
    with pytest.raises(ValueError):
        for i in elements:
            a = FieldElement(*i)

def test_valid(fieldelement):
    elements = fieldelement[0]
    for i in elements:
        a = FieldElement(*i)

def test_equal(fieldelement):
    a = fieldelement[0][0]
    b = fieldelement[0][0]
    c = fieldelement[0][1]
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
   
def test_Point_on_curve():
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
    # self != other
    assert e + f == c
    # self == other, y != 0
    assert f + f == g
    # self == other, y == 0
    assert d + d == Point(None, None, 6, 7)

def test_S256Point_infinity():

    p = S256Point(None, None)

    assert p.x == None

def test_S256Point_on_curve():

    valid_points = ((192, 49595586433674346371396676657723195126542195230466278338713869241189108741795), (25, 1102551495006820024539592786237854453433258304779672753607085440481650452602))
    invalid_points = ((200, 119), (42, 99))
    for x_raw, y_raw in valid_points:
        x = S256Field(x_raw)
        y = S256Field(y_raw)
        S256Point(x, y)
    for x_raw, y_raw in invalid_points:
        x = S256Field(x_raw)
        y = S256Field(y_raw)
        with pytest.raises(ValueError):
            S256Point(x, y)

def test_S256Point_order():

    p = N * G

    assert p.x == None

