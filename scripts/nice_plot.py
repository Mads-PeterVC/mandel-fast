import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from PIL import Image
from mandel_fast import py_mandelbrot, rs_mandelbrot, rs_mandelbrot_parallel

if __name__ == '__main__':
    extent = (-2.0, 1.0, -1.2, 1.2)
    aspect_ratio = (extent[1] - extent[0]) / (extent[3] - extent[2])

    width = 3840
    height = int(width / aspect_ratio)
    max_iter = 256

    img = rs_mandelbrot_parallel(width, height, max_iter, *extent)

    # Save at computed resolution using PIL (no DPI involved).
    img_min = float(img.min())
    img_max = float(img.max())
    if img_max > img_min:
        norm = (img.astype(np.float32) - img_min) / (img_max - img_min)
    else:
        norm = np.zeros_like(img, dtype=np.float32)
    # Mild gamma to bring out mid-tones.
    norm = np.power(norm, 0.6)

    cmap = LinearSegmentedColormap.from_list(
        'custom_cmap',
        ['#000000', '#24004d', '#4b0082', '#7a2cff', 'mediumpurple', '#f0d8ff'],
        N=256,
    )

    rgb = cmap(norm)[..., :3].astype(np.float32)
    rgb = np.clip(rgb, 0.0, 1.0)
    rgb8 = (rgb * 255).astype(np.uint8)
    Image.fromarray(rgb8, mode='RGB').save('mandelbrot_rust_parallel.png')


    # plt.imshow(img, extent=extent, cmap='hot')
    # plt.colorbar(label='Iteration count')
    # plt.title('Mandelbrot Set')
    # plt.xlabel('Real')
    # plt.ylabel('Imaginary')
    # plt.tight_layout()
    # plt.show()

    # plt.axis('off')
    # plt.savefig('mandelbrot_rust_parallel.pdf')
