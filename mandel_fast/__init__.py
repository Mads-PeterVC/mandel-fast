from .py_impl import py_mandelbrot
from .rust_impl import rs_mandelbrot, rs_mandelbrot_parallel

__all__ = ["py_mandelbrot", "rs_mandelbrot", "rs_mandelbrot_parallel"]
