from .main import main
import rich_click as click


@main.command()
@click.option(
    "--extent",
    "-e",
    nargs=4,
    type=tuple[float, float, float, float],
    default=[-2.0, 1.0, -1.5, 1.5],
    help="The extent of the complex plane to render: xmin xmax ymin ymax",
)
@click.option(
    "--width",
    "-w",
    type=int,
    default=800,
    help="The width of the output image in pixels",
)
@click.option(
    "--height",
    "-h",
    type=int,
    default=600,
    help="The height of the output image in pixels",
)
@click.option(
    "--max-iterations",
    "-m",
    type=int,
    default=255,
    help="The maximum number of iterations for the Mandelbrot calculation",
)
@click.option("--output", "-o", type=click.Path(), help="The output file path")
@click.option(
    "--method",
    "-M",
    type=click.Choice(["python", "rust", "rust_parallel"], case_sensitive=False),
    default="rust_parallel",
)
def render(
    extent: tuple[float, float, float, float],
    width: int,
    height: int,
    max_iterations: int,
    output: str,
    method: str,
):
    """Render the Mandelbrot set."""
    from mandel_fast import py_mandelbrot, rs_mandelbrot, rs_mandelbrot_parallel
    from PIL import Image


    if method == "python":
        mandelbrot_func = py_mandelbrot
    elif method == "rust":
        mandelbrot_func = rs_mandelbrot
    elif method == "rust_parallel":
        mandelbrot_func = rs_mandelbrot_parallel
    else:
        raise ValueError(f"Unknown method: {method}")
    
    extent_dict = {
        "xmin": extent[0],
        "xmax": extent[1],
        "ymin": extent[2],
        "ymax": extent[3],
    }
    
    image = mandelbrot_func(width=width, height=height, max_iter=max_iterations, **extent_dict)

    output_name = output or f"mandelbrot_{method}_{width}x{height}.png"

    img = Image.fromarray(image)
    img.save(output_name)
    print(f"Saved image to {output_name}")