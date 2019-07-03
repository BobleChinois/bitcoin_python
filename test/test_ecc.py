import pytest

from ecc.ecc import FieldElement

def test_FieldElement_valid():

    with pytest.raises(ValueError):
        a = FieldElement(6, -13)
        b = FieldElement(21, 17)
        c = FieldElement(-5, 23)

    
