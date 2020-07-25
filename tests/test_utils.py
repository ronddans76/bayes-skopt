from numpy.testing import assert_almost_equal
from skopt.learning.gaussian_process.kernels import (
    Matern,
    ConstantKernel,
    WhiteKernel,
    Exponentiation,
)
from bask.utils import guess_priors, construct_default_kernel


def test_construct_default_kernel():
    kernel = construct_default_kernel([0, 1])
    assert len(kernel.theta) == 3


def test_guess_priors():
    """Construct a complicated kernel and check if priors are constructed
    correctly."""
    kernel = Exponentiation(
        ConstantKernel(constant_value_bounds="fixed") * Matern()
        + WhiteKernel(),
        2.0,
    )

    priors = guess_priors(kernel)

    assert len(priors) == 2
    expected = [
        -0.02116327824572739,
        -2.112906921232193,
    ]
    for p, v in zip(priors, expected):
        assert_almost_equal(p(-0.9), v)
