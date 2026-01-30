import numpy as np


def mandel_escape(cx: float, cy: float, max_iter: int) -> int:
    """
    Determine the number of iterations for a point (cx, cy) to escape the Mandelbrot set.

    Parameters
    -----------
    cx : float
        Real part of the complex number.
    cy : float
        Imaginary part of the complex number.
    max_iter : int
        Maximum number of iterations to determine set membership.
    """
    zx = 0.0
    zy = 0.0
    it = 0
    while zx * zx + zy * zy <= 4.0 and it < max_iter:
        zx, zy = zx * zx - zy * zy + cx, 2.0 * zx * zy + cy
        it += 1
    return it


def py_mandelbrot(
    width: int,
    height: int,
    max_iter: int,
    xmin: float,
    xmax: float,
    ymin: float,
    ymax: float,
) -> np.ndarray:
    """
    Compute a Mandelbrot set image using pure Python.

    Parameters
    -----------
    width : int
        Width of the output image in pixels.
    height : int
        Height of the output image in pixels.
    max_iter : int
        Maximum number of iterations to determine set membership.
    xmin : float
        Minimum x-coordinate (real part).
    xmax : float
        Maximum x-coordinate (real part).
    ymin : float
        Minimum y-coordinate (imaginary part).
    ymax : float
        Maximum y-coordinate (imaginary part).
    """

    out = np.empty((height, width), dtype=np.uint16)
    for j in range(height):
        y = ymin + (ymax - ymin) * j / max(height - 1, 1)
        for i in range(width):
            x = xmin + (xmax - xmin) * i / max(width - 1, 1)
            out[j, i] = mandel_escape(x, y, max_iter)
    return out
