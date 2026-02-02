import numpy as np


def np_mandelbrot(
    width: int,
    height: int,
    max_iter: int,
    xmin: float,
    xmax: float,
    ymin: float,
    ymax: float,
) -> np.ndarray:
    """
    Compute a Mandelbrot set image using NumPy

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

    out = np.zeros((height, width), dtype=np.uint16)

    i = np.arange(width, dtype=np.float64)
    j = np.arange(height, dtype=np.float64)
    x = xmin + (xmax - xmin) * i / max(width - 1, 1)
    y = ymin + (ymax - ymin) * j / max(height - 1, 1)
    X, Y = np.meshgrid(x, y)

    C = X + 1j * Y
    Z = np.zeros((height, width), dtype=np.complex128)

    mask = np.full((height, width), True, dtype=bool)
    for _ in range(max_iter):
        out[mask] += 1
        Z[mask] = Z[mask] * Z[mask] + C[mask]
        escaped = (Z.real * Z.real + Z.imag * Z.imag) > 4.0
        mask &= ~escaped
        if not mask.any():
            break

    out[mask] = max_iter
    return out
