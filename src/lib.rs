use pyo3::prelude::*;
use rayon::prelude::*;
use rayon::ThreadPoolBuilder;

fn mandel_escape(cx: f64, cy: f64, max_iter: u16) -> u16 {
    let mut x = 0.0_f64;
    let mut y = 0.0_f64;
    let mut i: u16 = 0;

    while (x * x + y * y <= 4.0) && (i < max_iter) {
        let x_new = x * x - y * y + cx;
        y = 2.0 * x * y + cy;
        x = x_new;
        i += 1;
    }
    i
}

#[pyfunction]
fn mandelbrot(
    width: usize,
    height: usize,
    max_iter: u16,
    xmin: f64,
    xmax: f64,
    ymin: f64,
    ymax: f64,
) -> PyResult<Vec<u8>> {
    let mut out = vec![0u8; width * height];

    for j in 0..height {
        let y = ymin + (ymax - ymin) * (j as f64) / ((height - 1).max(1) as f64);
        for i in 0..width {
            let x = xmin + (xmax - xmin) * (i as f64) / ((width - 1).max(1) as f64);
            let it = mandel_escape(x, y, max_iter);
            // map iterations to 0..255 for display
            let v = if max_iter <= 255 { it as u8 } else { (it.min(255)) as u8 };
            out[j * width + i] = v;
        }
    }

    Ok(out)
}

#[pyfunction]
fn mandelbrot_parallel(
    py: Python<'_>,
    width: usize,
    height: usize,
    max_iter: u16,
    xmin: f64,
    xmax: f64,
    ymin: f64,
    ymax: f64,
    threads: Option<usize>, // None => Rayon default; Some(1) => effectively single-threaded
) -> PyResult<Vec<u8>> {
    if width == 0 || height == 0 {
        return Ok(Vec::new());
    }

    // Allocate output (row-major)
    let mut out = vec![0u8; width * height];

    // Build a pool only if user requests an explicit thread count.
    // This keeps the default behavior simple and avoids global thread-pool fiddling.
    let maybe_pool = match threads {
        Some(n) if n >= 1 => Some(
            ThreadPoolBuilder::new()
                .num_threads(n)
                .build()
                .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(e.to_string()))?,
        ),
        _ => None,
    };

    // Release the GIL while computing (important when you parallelize).
    py.allow_threads(|| {
        let mut compute = || {
            // Parallelize by rows: each thread fills one or more rows.
            out.par_chunks_mut(width)
                .enumerate()
                .for_each(|(j, row)| {
                    let y = ymin + (ymax - ymin) * (j as f64) / ((height - 1).max(1) as f64);
                    for i in 0..width {
                        let x = xmin + (xmax - xmin) * (i as f64) / ((width - 1).max(1) as f64);
                        let it = mandel_escape(x, y, max_iter);
                        let v = if max_iter <= 255 { it as u8 } else { it.min(255) as u8 };
                        row[i] = v;
                    }
                });
        };

        if let Some(pool) = maybe_pool.as_ref() {
            pool.install(compute);
        } else {
            compute();
        }
    });

    Ok(out)
}

#[pymodule]
fn _rust(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(mandelbrot, m)?)?;
    m.add_function(wrap_pyfunction!(mandelbrot_parallel, m)?)?;
    Ok(())
}
