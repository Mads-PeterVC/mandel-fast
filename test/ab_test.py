import numpy as np

def test_rs_mandelbrot_vs_py(py_mandelbrot_result, rs_mandelbrot_result):
    """Test that the Rust mandelbrot implementation matches the Python one."""
    np.testing.assert_array_equal(rs_mandelbrot_result, py_mandelbrot_result)

def test_rs_mandelbrot_parallel_vs_py(py_mandelbrot_result, rs_mandelbrot_parallel_result):
    """Test that the Rust parallel mandelbrot implementation matches the Python one."""
    np.testing.assert_array_equal(rs_mandelbrot_parallel_result, py_mandelbrot_result)

def test_np_mandelbrot_vs_py(py_mandelbrot_result, np_mandelbrot_result):
    """Test that the NumPy mandelbrot implementation matches the Python one."""
    np.testing.assert_array_equal(np_mandelbrot_result, py_mandelbrot_result)
