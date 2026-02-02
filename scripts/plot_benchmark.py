import matplotlib.pyplot as plt
import numpy as np

def adjust_plt_params():
    plt.rcParams.update({
        'font.size': 14,
        'axes.titlesize': 16,
        'axes.labelsize': 14,
        'legend.fontsize': 14,
        'figure.dpi': 200,
        'lines.linewidth': 3,
        'lines.markersize': 7,
    })

def plot_benchmark_results(npz_file='bench_results.npz', output_file='benchmark_plot.png'):
    data = np.load(npz_file)
    pixels = data['pixels']
    py_times = data['py_times']
    rs_times = data['rs_times']
    rs_parallel_times = data['rs_parallel_times']
    np_times = data['np_times']

    fig, axes = plt.subplots(1, 2, figsize=(12, 6), layout='constrained')


    ax = axes[0]
    ax.plot(pixels, py_times, 'o-', label='Python Implementation', color='blue')
    ax.plot(pixels, np_times, 'x-', label='NumPy Implementation', color='red')
    ax.plot(pixels, rs_times, 's-', label='Rust Implementation', color='orange')
    ax.plot(pixels, rs_parallel_times, '^-', label='Rust Parallel Implementation', color='green')
    ax.set_ylabel('Time (seconds)')
    ax.set_xlabel('Number of Pixels')
    ax.set_xscale('log')
    ax.legend(framealpha=0.5)

    # Second subplot: Speedup
    ax = axes[1]
    ax.plot(pixels, py_times / rs_times, 's-', label='Rust Speedup', color='orange')
    ax.plot(pixels, py_times / np_times, 'x-', label='NumPy Speedup', color='red')
    ax.plot(pixels, py_times / rs_parallel_times, '^-', label='Rust Parallel Speedup', color='green')
    ax.set_ylabel('Speedup (Python Time / Rust Time)')
    ax.set_xlabel('Number of Pixels')
    ax.set_xscale('log')
    ax.legend(framealpha=0.5)

    fig.savefig(output_file, transparent=True, bbox_inches='tight')




if __name__ == '__main__':
    adjust_plt_params()
    plot_benchmark_results()