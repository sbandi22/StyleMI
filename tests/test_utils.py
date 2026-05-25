import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

import pytest
from fastapi import HTTPException
from utils.validators import validate_occasion, VALID_OCCASIONS


def test_valid_occasion():
    for occ in VALID_OCCASIONS:
        validate_occasion(occ)


def test_invalid_occasion():
    with pytest.raises(HTTPException):
        validate_occasion("spacesuit")
