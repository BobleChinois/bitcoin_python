import pytest

from ecc.ecc import FieldElement


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
