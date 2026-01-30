import numpy as np

def py_mandelbrot(width, height, max_iter, xmin, xmax, ymin, ymax):
    out = np.empty((height, width), dtype=np.uint16)
    for j in range(height):
        y = ymin + (ymax - ymin) * j / max(height - 1, 1)
        for i in range(width):
            x = xmin + (xmax - xmin) * i / max(width - 1, 1)
            zx = 0.0
            zy = 0.0
            it = 0
            while zx*zx + zy*zy <= 4.0 and it < max_iter:
                zx, zy = zx*zx - zy*zy + x, 2.0*zx*zy + y
                it += 1
            out[j, i] = it
    return out
