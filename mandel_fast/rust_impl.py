from ._rust import mandelbrot as _rs_mandelbrot
from ._rust import mandelbrot_parallel as _rs_mandelbrot_parallel

import numpy as np

def rs_to_array(buf, width, height):
    # buf is a list/Vec[u8] returned via PyO3; turn into ndarray
    arr = np.frombuffer(bytes(buf), dtype=np.uint8).reshape((height, width))
    return arr

def rs_mandelbrot_parallel(width: int, height: int, max_iter: int,
                           xmin: float, xmax: float,
                           ymin: float, ymax: float, threads: int | None = None) -> np.ndarray:
    buf = _rs_mandelbrot_parallel(width, height, max_iter, xmin, xmax, ymin, ymax, threads)
    return rs_to_array(buf, width, height)

def rs_mandelbrot(width: int, height: int, max_iter: int,
                    xmin: float, xmax: float,
                    ymin: float, ymax: float) -> np.ndarray:
        buf = _rs_mandelbrot(width, height, max_iter, xmin, xmax, ymin, ymax)
        return rs_to_array(buf, width, height)

