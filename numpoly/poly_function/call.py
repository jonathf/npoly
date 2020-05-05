"""Evaluate polynomial."""
import logging
import numpy
import numpoly


def call(poly, *args, **kwargs):
    """
    Evaluate polynomial by inserting new values in to the indeterminants.

    Equivalent to calling the polynomial or using the ``__call__`` method.

    Args:
        poly (numpoly.ndpoly):
            Polynomial to evaluate.
        args (int, float, numpy.ndarray, numpoly.ndpoly):
            Argument to evaluate indeterminants. Ordered positional by
            ``poly.indeterminants``.
        kwargs (int, float, numpy.ndarray, numpoly.ndpoly):
            Same as ``args``, but positioned by name.

    Returns:
        (Union[numpy.ndarray, numpoly.ndpoly]):
            Evaluated polynomial. If the resulting array does not contain any
            indeterminants, an array is returned instead of a polynomial.

    Examples:
        >>> x, y = numpoly.symbols("x y")
        >>> poly = numpoly.polynomial([[x, x-1], [y, y+x]])
        >>> poly()
        polynomial([[x, -1+x],
                    [y, x+y]])
        >>> poly
        polynomial([[x, -1+x],
                    [y, x+y]])
        >>> poly(1, 0)
        array([[1, 0],
               [0, 1]])
        >>> poly(1, y=[0, 1, 2])
        array([[[1, 1, 1],
                [0, 0, 0]],
        <BLANKLINE>
               [[0, 1, 2],
                [1, 2, 3]]])
        >>> poly(y)
        polynomial([[y, -1+y],
                    [y, 2*y]])
        >>> poly(y=x-1, x=2*y)
        polynomial([[2*y, -1+2*y],
                    [-1+x, -1+2*y+x]])

    """
    logger = logging.getLogger(__name__)

    # Make sure kwargs contains all args and nothing but indeterminants:
    for arg, indeterminant in zip(args, poly.names):
        if indeterminant in kwargs:
            raise TypeError(
                "multiple values for argument '%s'" % indeterminant)
        kwargs[indeterminant] = arg
    extra_args = [key for key in kwargs if key not in poly.names]
    if extra_args:
        raise TypeError("unexpected keyword argument '%s'" % extra_args[0])

    if not kwargs:
        return poly.copy()

    # Saturate kwargs with values not given:
    indeterminants = poly.indeterminants
    for indeterminant in indeterminants:
        name = indeterminant.names[0]
        if name not in kwargs:
            kwargs[name] = indeterminant

    # There can only be one shape:
    ones = numpy.ones((), dtype=int)
    for value in kwargs.values():
        ones = ones * numpy.ones(numpoly.polynomial(value).shape, dtype=int)
    shape = poly.shape+ones.shape

    logger.debug("poly shape: %s", poly.shape)
    logger.debug("kwargs common shape: %s", ones.shape)
    logger.debug("output shape: %s", shape)

    # main loop:
    out = 0
    for exponent, coefficient in zip(poly.exponents, poly.coefficients):
        term = ones
        for power, name in zip(exponent, poly.names):
            term = term*kwargs[name]**power
        if isinstance(term, numpoly.ndpoly):
            tmp = numpoly.outer(coefficient, term)
        else:
            tmp = numpy.outer(coefficient, term)
        out = out+tmp.reshape(shape)

    if isinstance(out, numpoly.ndpoly):
        if out.isconstant():
            return out.tonumpy()
        out, _ = numpoly.align_indeterminants(out, indeterminants)
        return out
    return out
