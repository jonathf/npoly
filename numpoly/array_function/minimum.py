"""Element-wise minimum of array elements."""
import numpy
import numpoly

from ..dispatch import implements


@implements(numpy.minimum)
def minimum(x1, x2, out=None, **kwargs):
    """
    Element-wise minimum of array elements.

    Compare two arrays and returns a new array containing the element-wise
    minima. If one of the elements being compared is a NaN, then that
    element is returned. If both elements are NaNs then the first is
    returned. The latter distinction is important for complex NaNs, which
    are defined as at least one of the real or imaginary parts being a NaN.
    The net effect is that NaNs are propagated.

    Args:
        x1, x2 (numpoly.ndpoly):
            The arrays holding the elements to be compared. If ``x1.shape !=
            x2.shape``, they must be broadcastable to a common shape (which
            becomes the shape of the output).
        out (numpoly.ndarray, Tuple[numpoly.ndarray, numpoly.ndarray], None):
            A location into which the result is stored. If provided, it must
            have a shape that the inputs broadcast to. If not provided or
            `None`, a freshly-allocated array is returned. A tuple (possible
            only as a keyword argument) must have length equal to the number of
            outputs.
        where (Optional[numpy.ndarray]):
            This condition is broadcast over the input. At locations where the
            condition is True, the `out` array will be set to the ufunc result.
            Elsewhere, the `out` array will retain its original value. Note
            that if an uninitialized `out` array is created via the default
            ``out=None``, locations within it where the condition is False will
            remain uninitialized.
        kwargs:
            Keyword args passed to numpy.ufunc.

    Returns:
        (numpoly.ndarray):
            The minimum of `x1` and `x2`, element-wise. This is a scalar if
            both `x1` and `x2` are scalars.

    Examples:
        >>> x, y = numpoly.symbols("x y")
        >>> numpoly.minimum(3, 4)
        polynomial(3)
        >>> numpoly.minimum(4*x, 3*x)
        polynomial(3*x)
        >>> numpoly.minimum(x, y)
        polynomial(x)
        >>> numpoly.minimum(x**2, x)
        polynomial(x)
        >>> numpoly.minimum([1, x, x**2, x**3], y)
        polynomial([1, x, y, y])
        >>> numpoly.minimum(x+1, x-1)
        polynomial(x-1)

    """
    x1, x2 = numpoly.align_polynomials(x1, x2)
    coefficients1 = x1.coefficients
    coefficients2 = x2.coefficients
    out = numpy.zeros(x1.shape, dtype=bool)
    for idx in numpoly.bsort(x1.exponents.T, ordering="GR"):
        indices = (coefficients1[idx] != 0) | (coefficients2[idx] != 0)
        indices &= coefficients1[idx] != coefficients2[idx]
        out[indices] = coefficients1[idx][indices] < coefficients2[idx][indices]
    return numpoly.where(out, x1, x2)
