"""Return the minimum of an array or minimum along an axis."""
import numpy
import numpoly

from ..dispatch import implements


@implements(numpy.amin)
def amin(a, axis=None, out=None, **kwargs):
    """
    Return the minimum of an array or minimum along an axis.

    Args:
        a (numpoly.ndpoly):
            Input data.
        axis (int, Tuple[int], None):
            Axis or axes along which to operate.  By default, flattened input
            is used. If this is a tuple of ints, the minimum is selected over
            multiple axes, instead of a single axis or all the axes as before.
        out (Optional[numpoly.ndpoly]):
            Alternative output array in which to place the result. Must be of
            the same shape and buffer length as the expected output.
        keepdims (Optional[bool]):
            If this is set to True, the axes which are reduced are left in the
            result as dimensions with size one. With this option, the result
            will broadcast correctly against the input array.

            If the default value is passed, then `keepdims` will not be passed
            through to the `amax` method of sub-classes of `ndarray`, however
            any non-default value will be.  If the sub-class' method does not
            implement `keepdims` any exceptions will be raised.
        initial (int, float, complex, numpoly.ndpoly):
            The minimum value of an output element. Must be present to allow
            computation on empty slice.
        where : array_like of bool, optional
            Elements to compare for the maximum.

    Returns:
        (numpy.ndarray):
            Minimum of `a`. If `axis` is None, the result is a scalar value.
            If `axis` is given, the result is an array of dimension
            ``a.ndim-1``.

    Examples:
        >>> x, y = numpoly.symbols("x y")
        >>> numpoly.amin([13, 7])
        polynomial(7)
        >>> numpoly.amin([1, x, x**2, y])
        polynomial(1)
        >>> numpoly.amin([x, y, x**2])
        polynomial(x)
        >>> numpoly.amin([[3*x**2, x**2], [2*x**2, 4*x**2]], axis=1)
        polynomial([x**2, 2*x**2])

    """
    del out
    a = numpoly.aspolynomial(a)
    proxy = numpoly.sortable_proxy(a, ordering="GR")
    indices = numpy.amin(proxy, axis=axis, **kwargs)
    out = a[numpy.isin(proxy, indices)]
    out = out[numpy.argsort(indices.ravel())]
    return out.reshape(indices.shape)
