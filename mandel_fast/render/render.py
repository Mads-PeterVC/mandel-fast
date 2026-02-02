from mandel_fast import py_mandelbrot, rs_mandelbrot, rs_mandelbrot_parallel
from dataclasses import dataclass
from PIL import Image
import numpy as np
from matplotlib.colors import LinearSegmentedColormap


@dataclass
class RenderConfig:
    width: int
    height: int
    extent: tuple[float, float, float, float]  # (xmin, xmax, ymin, ymax)
    max_iter: int
    method: str = "rust_parallel"  # 'python', 'rust', or 'rust_parallel'


def render_mandelbrot(config: RenderConfig) -> Image:

    # Select the appropriate Mandelbrot implenentation
    if config.method == "python":
        mandelbrot_func = py_mandelbrot
    elif config.method == "rust":
        mandelbrot_func = rs_mandelbrot
    elif config.method == "rust_parallel":
        mandelbrot_func = rs_mandelbrot_parallel
    else:
        raise ValueError(f"Unknown method: {config.method}")
    
    # Call the selected Mandelbrot function
    mandelbrot_data = mandelbrot_func(
        width=config.width,
        height=config.height,
        xmin=config.extent[0],
        xmax=config.extent[1],
        ymin=config.extent[2],
        ymax=config.extent[3],
        max_iter=config.max_iter
    )

    # Convert the raw data to a PIL Image
    img_min = float(mandelbrot_data.min())
    img_max = float(mandelbrot_data.max())
    if img_max > img_min:
        norm = (mandelbrot_data.astype(np.float32) - img_min) / (img_max - img_min)
    else:
        norm = np.zeros_like(mandelbrot_data, dtype=np.float32)

    norm = np.power(norm, 0.6)
    cmap = LinearSegmentedColormap.from_list(
        'custom_cmap',
        ['#000000', '#24004d', '#4b0082', '#7a2cff', 'mediumpurple', '#f0d8ff'],
        N=256,
    )

    rgb = cmap(norm)[..., :3].astype(np.float32)
    rgb = np.clip(rgb, 0.0, 1.0)
    rgb8 = (rgb * 255).astype(np.uint8)
    image = Image.fromarray(rgb8, mode='RGB')

    return image

if __name__ == '__main__':
    extent = (-2.0, 1.0, -1.2, 1.2)
    aspect_ratio = (extent[1] - extent[0]) / (extent[3] - extent[2])

    width = 3840
    height = int(width / aspect_ratio)
    max_iter = 255

    config = RenderConfig(
        width=width,
        height=height,
        extent=extent,
        max_iter=max_iter,
        method="rust_parallel"
    )

    img = render_mandelbrot(config)
    img.save('mandelbrot_rust_parallel.png')