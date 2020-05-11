"""Return the indices of the maximum values along an axis."""
import numpy
import numpoly

from ..dispatch import implements


@implements(numpy.argmax)
def argmax(a, axis=None, out=None, **kwargs):
    """
    Return the indices of the maximum values along an axis.

    As polynomials are not inherently sortable, values are sorted using the
    highest `lexicographical` ordering. Between the values that have the same
    highest ordering, the elements are sorted using the coefficients. This also
    ensures that the method behaves as expected with ``numpy.ndarray``.

    Args:
        a (numpoly.ndpoly):
            Input array.
        axis (Optional[int]):
            By default, the index is into the flattened array, otherwise along
            the specified axis.
        out (Optional[numpoly.ndpoly]):
            If provided, the result will be inserted into this array. It should
            be of the appropriate shape and dtype.

    Returns:
        (numpy.ndarray, int):
            Array of indices into the array. It has the same shape as `a.shape`
            with the dimension along `axis` removed.

    Notes:
        In case of multiple occurrences of the maximum values, the
        indices corresponding to the first occurrence are returned.

    Examples:
        >>> x, y = numpoly.symbols("x y")
        >>> numpoly.argmax([13, 7])
        0
        >>> numpoly.argmax([1, x, x**2, y])
        2
        >>> numpoly.argmax([1, x, y])
        2
        >>> numpoly.argmax([[3*x**2, x**2], [2*x**2, 4*x**2]], axis=0)
        array([0, 1])

    """
    proxy = numpoly.sortable_proxy(a, ordering="GR")
    return numpy.argmax(proxy, axis=axis, out=out, **kwargs)
