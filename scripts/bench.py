import time
import numpy as np
import matplotlib.pyplot as plt
from mandel_fast import (
    py_mandelbrot,
    rs_mandelbrot,
    rs_mandelbrot_parallel,
    np_mandelbrot,
)


def time_fn(fn, repeats=5):
    times = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        res = fn()
        # use result to avoid any "oops it got optimized away" kind of issues
        if isinstance(res, np.ndarray):
            _ = int(res[0, 0])
        else:
            _ = int(res[0])
        times.append(time.perf_counter() - t0)
    return float(np.median(times))


def main():
    # 2) Timing sweep
    sizes = [50, 100, 200, 300, 400, 600, 800, 1000, 1200, 1600, 2000, 2500]
    extent = (-2.0, 1.0, -1.2, 1.2)
    max_iter = 255

    py_times, np_times, rs_times, rs_parallel_times = [], [], [], []

    for s in sizes:
        w = h = s

        py_t = time_fn(lambda: py_mandelbrot(w, h, max_iter, *extent), repeats=3)
        np_t = time_fn(lambda: np_mandelbrot(w, h, max_iter, *extent), repeats=3)
        rs_t = time_fn(lambda: rs_mandelbrot(w, h, max_iter, *extent), repeats=5)
        rs_parallel_t = time_fn(
            lambda: rs_mandelbrot_parallel(w, h, max_iter, *extent), repeats=5
        )
        np_times.append(np_t)
        py_times.append(py_t)
        rs_times.append(rs_t)
        rs_parallel_times.append(rs_parallel_t)

    pixels = np.array(sizes, dtype=float) ** 2

    results = {
        "pixels": pixels,
        "py_times": np.array(py_times),
        "rs_times": np.array(rs_times),
        "rs_parallel_times": np.array(rs_parallel_times),
        "np_times": np.array(np_times),
    }

    np.savez("bench_results.npz", **results)


if __name__ == "__main__":
    main()
