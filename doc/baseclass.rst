Baseclass
=========

The core element of the `numpoly` library is the `numpoly.ndpoly` class. The
class is subclass of of the `numpy.ndarray` and the implementation follows the
recommendation of how to subclass `numpy` objects.

In a nutshell, the `nmply.ndpoly` under the hood is a structured array, where
the column names represents the exponent powers as strings, and the values
represents the coefficients. In other words, the polynomial coefficients are
represented as `numpy.ndarray`:

.. math::

    P(x_1, \dots, x_D) = \sum_{n=1}^N c_n \prod_{d=1}^D x_d^{p_{nd}}

Where :math:`P` is polynomial vector, :math:`N` is the number of terms in the
polynomial sum, :math:`c_n` is a (potentially) multi-dimensional polynomial
coefficients, :math:`x_d` is the :math:`d`-th indeterminant name, and
:math:`p_{nd}` is the exponent for the :math:`n`-th polynomial term and the
:math:`d`-th indeterminant name.

For example, for a simple polynomial with scalar coefficients:

.. code:: python

    >>> x, y = numpoly.symbols("x y")
    >>> poly = numpoly.polynomial(4*x+3*y-1)
    >>> poly
    polynomial(-1+4*x+3*y)
    >>> poly.coefficients
    [-1, 4, 3]
    >>> poly.exponents
    array([[0, 0],
           [1, 0],
           [0, 1]], dtype=uint32)
    >>> poly.indeterminants
    polynomial([x, y])

These three properties can be used to reconstruct the polynomial:

.. code:: python

    >>> terms = numpoly.prod(
    ...     poly.indeterminants**poly.exponents, -1)*poly.coefficients
    >>> terms
    polynomial([-1, 4*x, 3*y])
    >>> numpoly.sum(terms, 0)
    polynomial(-1+3*y+4*x)


Though not for any practical reasons, but it is possible to view the polynomial
in it's true form:

.. code:: python

    >>> dtype = [(key, poly.dtype) for key in poly.keys]
    >>> array = numpy.ndarray(
    ...     shape=poly.shape, dtype=dtype, buffer=poly.data)
    >>> array  # doctest: +NORMALIZE_WHITESPACE
    array((-1, 4, 3), dtype=[('00', '<i8'), ('10', '<i8'), ('01', '<i8')])

Which, together with the indeterminant names, can be cast back to a polynomial:

.. code:: python

    >>> numpoly.aspolynomial(array, names=("x", "y"))
    polynomial(-1+4*x+3*y)

.. autoclass:: numpoly.baseclass.ndpoly
