"""Test for `numpoly.construct`."""
from pytest import raises
import numpy

import numpoly
from numpoly.construct.clean import (
    postprocess_attributes, PolynomialConstructionError)

X, Y = XY = numpoly.symbols("X Y")


def test_postprocess_attributes():
    """Test related to polynomial construction from attributes."""
    with raises(PolynomialConstructionError):  # exponent.ndim too small
        postprocess_attributes(numpy.arange(2), [1, 2])
    with raises(PolynomialConstructionError):  # exponent.ndim too large
        postprocess_attributes(numpy.arange(24).reshape(2, 3, 4), [1, 2])
    with raises(PolynomialConstructionError):  # exponents len incompatible with coefficients
        postprocess_attributes(numpy.arange(6).reshape(2, 3), [1, 2, 3])
    with raises(PolynomialConstructionError):  # duplicate exponents
        postprocess_attributes([[1], [1]], [1, 2])
    with raises(PolynomialConstructionError):  # exponents len incompatible with name length
        postprocess_attributes([[1], [2]], [1, 2], ["x", "y", "z"])
    with raises(PolynomialConstructionError):  # duplicate names
        postprocess_attributes([[1, 1]], [1], ["x", "x"])


def test_aspolynomial():
    poly = 2*X-Y+1
    assert poly == numpoly.aspolynomial(poly)
    assert poly == numpoly.aspolynomial(poly, names=XY)
    assert poly == numpoly.aspolynomial(poly.todict(), names=XY)
    assert poly == numpoly.aspolynomial(poly, names=("X", "Y"))
    assert numpy.all(numpoly.symbols("Z:2") == numpoly.aspolynomial(XY, names="Z"))
    assert poly == numpoly.aspolynomial(poly.todict(), names=("X", "Y"))
    assert poly != numpoly.aspolynomial(poly.todict(), names=("Y", "X"))
    assert X == numpoly.aspolynomial(Y, names="X")
    assert poly != numpoly.aspolynomial(poly.todict(), names="X")
    assert isinstance(numpoly.aspolynomial([1, 2, 3]), numpoly.ndpoly)
    assert numpy.all(numpoly.aspolynomial([1, 2, 3]) == [1, 2, 3])
