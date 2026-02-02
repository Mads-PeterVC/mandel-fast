from mandel_fast.render.render import RenderConfig
from rich.progress import track


def _apply_easing(t: float, easing: str) -> float:
    if easing == "linear":
        return t
    if easing == "ease_in_out":
        # Smoothstep
        return t * t * (3 - 2 * t)
    if easing == "ease_in":
        return t * t
    if easing == "ease_out":
        return 1 - (1 - t) * (1 - t)
    raise ValueError(f"Unknown easing: {easing}")


def _interpolate_extent(
    start_extent: tuple[float, float, float, float],
    end_extent: tuple[float, float, float, float],
    t: float,
    mode: str,
) -> tuple[float, float, float, float]:
    if mode == "linear":
        xmin = start_extent[0] + t * (end_extent[0] - start_extent[0])
        xmax = start_extent[1] + t * (end_extent[1] - start_extent[1])
        ymin = start_extent[2] + t * (end_extent[2] - start_extent[2])
        ymax = start_extent[3] + t * (end_extent[3] - start_extent[3])
        return (xmin, xmax, ymin, ymax)

    if mode == "log_zoom":
        # Interpolate center linearly, size exponentially (constant zoom ratio per frame)
        sxmin, sxmax, symin, symax = start_extent
        exmin, exmax, eymin, eymax = end_extent

        scx = (sxmin + sxmax) / 2.0
        scy = (symin + symax) / 2.0
        ecx = (exmin + exmax) / 2.0
        ecy = (eymin + eymax) / 2.0

        sdx = sxmax - sxmin
        sdy = symax - symin
        edx = exmax - exmin
        edy = eymax - eymin

        if sdx <= 0 or sdy <= 0 or edx <= 0 or edy <= 0:
            raise ValueError(
                "Extent sizes must be positive for log_zoom interpolation."
            )

        cx = scx + t * (ecx - scx)
        cy = scy + t * (ecy - scy)

        dx = sdx * ((edx / sdx) ** t)
        dy = sdy * ((edy / sdy) ** t)

        return (cx - dx / 2.0, cx + dx / 2.0, cy - dy / 2.0, cy + dy / 2.0)

    raise ValueError(f"Unknown extent interpolation mode: {mode}")


def interpolate_configs(
    configs: list[RenderConfig],
    steps: list[int],
    easing: str = "linear",
    extent_mode: str = "linear",
) -> list[RenderConfig]:
    """
    Generate a list of RenderConfig objects by interpolating between given configurations.

    Parameters
    ----------
    configs : list[RenderConfig]
        A list of RenderConfig objects to interpolate between.
    steps : list[int]
        A list of integers specifying the number of interpolation steps between each pair of configurations.

    Returns
    -------
    list[RenderConfig]
        A list of interpolated RenderConfig objects.
    """
    if len(configs) < 2:
        raise ValueError("At least two configurations are required for interpolation.")
    if len(steps) != len(configs) - 1:
        raise ValueError("Steps length must be one less than configs length.")

    interpolated_configs = []

    for i in range(len(configs) - 1):
        start = configs[i]
        end = configs[i + 1]
        step_count = steps[i]

        for step in range(step_count):
            t = step / step_count
            t_eased = _apply_easing(t, easing)
            width = int(start.width + t_eased * (end.width - start.width))
            height = int(start.height + t_eased * (end.height - start.height))
            xmin, xmax, ymin, ymax = _interpolate_extent(
                start.extent,
                end.extent,
                t_eased,
                extent_mode,
            )
            max_iter = int(start.max_iter + t_eased * (end.max_iter - start.max_iter))

            new_config = RenderConfig(
                width=width,
                height=height,
                extent=(xmin, xmax, ymin, ymax),
                max_iter=max_iter,
                method=start.method,  # Assuming method remains the same
            )
            interpolated_configs.append(new_config)

    interpolated_configs.append(configs[-1])  # Include the last config
    return interpolated_configs


def point_zoom_interpolation(
    center: tuple[float, float],    
    dx: float,
    dy: float,
    zoom_factor: float,
) -> tuple[tuple[float, float, float, float], tuple[float, float, float, float]]:
    
    extent0 = (
        center[0] - dx / 2,
        center[0] + dx / 2,
        center[1] - dy / 2,
        center[1] + dy / 2,
    )
    extent1 = (
        center[0] - (dx / zoom_factor) / 2,
        center[0] + (dx / zoom_factor) / 2,
        center[1] - (dy / zoom_factor) / 2,
        center[1] + (dy / zoom_factor) / 2,
    )

    return extent0, extent1

def make_animation(
    configs: list[RenderConfig],
    steps: list[int],
    output_path: str,
    fps: int = 30,
    easing: str = "linear",
    extent_mode: str = "linear",    
    reverse: bool = False,
) -> None:
    """
    Create an animated GIF by rendering frames based on interpolated RenderConfig objects.

    Parameters
    ----------
    configs : list[RenderConfig]
        A list of RenderConfig objects to interpolate between.
    steps : list[int]
        A list of integers specifying the number of interpolation steps between each pair of configurations.
    output_path : str
        The file path to save the animated GIF.
    fps : int, optional
        Frames per second for the animation. Default is 30.
    easing : str, optional
        Easing function to use for interpolation. Default is "linear".
    extent_mode : str, optional
        Extent interpolation mode. Default is "linear". Can be "linear" or "log_zoom". 
        "log_zoom" makes zooming smoother by interpolating the extent sizes exponentially.
    reverse : bool, optional
        If True, the animation will play in reverse after reaching the end. Default is False.
    """
    frames = []
    interpolated_configs = interpolate_configs(
        configs,
        steps,
        easing=easing,
        extent_mode=extent_mode,
    )

    for cfg in track(
        interpolated_configs,
        description="Rendering frames...",
        total=len(interpolated_configs),
    ):
        img = render_mandelbrot(cfg)
        frames.append(img)

    if reverse:
        frames += frames[-2:0:-1]  # Exclude the last frame to avoid duplication

    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=int(1000 / fps),
        loop=0,
    )


if __name__ == "__main__":
    from mandel_fast.render.render import render_mandelbrot

    central_point = (
        -0.743643887037158704752191506114774,
        0.131825904205311970493132056385139,
    )

    # Example usage
    extent = (
        central_point[0] - 1.0,
        central_point[0] + 1.0,
        central_point[1] - 0.5,
        central_point[1] + 0.5,
    )
    aspect_ratio = (extent[1] - extent[0]) / (extent[3] - extent[2])

    width = int(1920 / 2)
    height = int(width / aspect_ratio)
    max_iter = 255

    config1 = RenderConfig(
        width=width,
        height=height,
        extent=extent,
        max_iter=max_iter,
        method="rust_parallel",
    )

    extent2 = (
        central_point[0] - 0.0005,
        central_point[0] + 0.0005,
        central_point[1] - 0.0004,
        central_point[1] + 0.0004,
    )

    config2 = RenderConfig(
        width=width,
        height=height,
        extent=extent2,
        max_iter=max_iter,
        method="rust_parallel",
    )

    make_animation(
        configs=[config1, config2],
        steps=[255],
        output_path="mandelbrot_zoom.gif",
        fps=30,
        easing="ease_in_out",
        extent_mode="log_zoom",
        reverse=True,
    )
