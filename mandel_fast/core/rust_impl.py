from ._rust import mandelbrot as _rs_mandelbrot
from ._rust import mandelbrot_parallel as _rs_mandelbrot_parallel

import numpy as np


def rs_to_array(buf, width, height):
    # buf is a list/Vec[u8] returned via PyO3; turn into ndarray
    arr = np.frombuffer(bytes(buf), dtype=np.uint8).reshape((height, width))
    return arr


def rs_mandelbrot_parallel(
    width: int,
    height: int,
    max_iter: int,
    xmin: float,
    xmax: float,
    ymin: float,
    ymax: float,
    threads: int | None = None,
) -> np.ndarray:
    """
    Compute the Mandelbrot set using the Rust parallel implementation.

    Parameters
    ----------
    width : int
        The width of the output image in pixels.
    height : int
        The height of the output image in pixels.
    max_iter : int
        The maximum number of iterations to perform for each point.
    xmin : float
        The minimum x-coordinate (real part) of the complex plane.
    xmax : float
        The maximum x-coordinate (real part) of the complex plane.
    ymin : float
        The minimum y-coordinate (imaginary part) of the complex plane.
    ymax : float
        The maximum y-coordinate (imaginary part) of the complex plane.
    threads : int | None, optional
        The number of threads to use for parallel computation. If None,
        the implementation will decide the optimal number of threads.
    """
    buf = _rs_mandelbrot_parallel(
        width, height, max_iter, xmin, xmax, ymin, ymax, threads
    )
    return rs_to_array(buf, width, height)


def rs_mandelbrot(
    width: int,
    height: int,
    max_iter: int,
    xmin: float,
    xmax: float,
    ymin: float,
    ymax: float,
) -> np.ndarray:
    """
    Compute the Mandelbrot set using the Rust single-threaded implementation.

    Parameters    
    ----------
    width : int
        The width of the output image in pixels.
    height : int
        The height of the output image in pixels.
    max_iter : int
        The maximum number of iterations to perform for each point.
    xmin : float
        The minimum x-coordinate (real part) of the complex plane.
    xmax : float
        The maximum x-coordinate (real part) of the complex plane.
    ymin : float
        The minimum y-coordinate (imaginary part) of the complex plane.
    ymax : float
        The maximum y-coordinate (imaginary part) of the complex plane.
    """

    buf = _rs_mandelbrot(width, height, max_iter, xmin, xmax, ymin, ymax)
    return rs_to_array(buf, width, height)
