"""Counts the number of non-zero values in the array a."""
import numpy
import numpoly

from ..dispatch import implements

@implements(numpy.count_nonzero)
def count_nonzero(q0, axis=None, **kwargs):
    """
    Count the number of non-zero values in the array a.

    Args:
        x (numpoly.ndpoly):
            The array for which to count non-zeros.
        axis: (Union[int, Tuple[int], None]):
            Axis or tuple of axes along which to count non-zeros. Default is
            None, meaning that non-zeros will be counted along a flattened
            version of a.

    Returns:
        count (Union[bool, numpy.ndarray]):
            Number of non-zero values in the array along a given axis.
            Otherwise, the total number of non-zero values in the array is
            returned.

    Examples:
        >>> q0, q1 = numpoly.variable(2)
        >>> numpoly.count_nonzero([q0])
        1
        >>> numpoly.count_nonzero([[0, q0, q0*q0, 0, 0],
        ...                        [q0+1, 0, 0, 2*q0, 19*q0]])
        5
        >>> numpoly.count_nonzero([[0, q0, 7*q0, 0, 0],
        ...                        [3*q1, 0, 0, 2, 19*q0+q1]], axis=0)
        array([1, 1, 1, 1, 1])
        >>> numpoly.count_nonzero([[0, q0, q1, 0, 0],
        ...                        [q0, 0, 0, 2*q0, 19*q1]], axis=1)
        array([2, 3])

    """
    a = numpoly.aspolynomial(q0)
    return numpy.count_nonzero(numpy.any(a.coefficients, axis=0), axis=axis)
