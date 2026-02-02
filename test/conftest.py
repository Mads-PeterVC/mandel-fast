import pytest
from mandel_fast import py_mandelbrot, rs_mandelbrot, rs_mandelbrot_parallel

@pytest.fixture(scope="module")
def mandelbrot_settings():
    extent = (-2.0, 1.0, -1.2, 1.2)
    width = 300
    height = 300
    max_iter = 255
    return width, height, max_iter, extent

@pytest.fixture()
def py_mandelbrot_result(mandelbrot_settings):
    width, height, max_iter, extent = mandelbrot_settings
    img = py_mandelbrot(width, height, max_iter, *extent)
    return img

@pytest.fixture()
def rs_mandelbrot_result(mandelbrot_settings):
    width, height, max_iter, extent = mandelbrot_settings
    img = rs_mandelbrot(width, height, max_iter, *extent)
    return img

@pytest.fixture()
def rs_mandelbrot_parallel_result(mandelbrot_settings):
    width, height, max_iter, extent = mandelbrot_settings
    img = rs_mandelbrot_parallel(width, height, max_iter, *extent)
    return img

