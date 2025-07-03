import matplotlib.pyplot as plt
import numpy as np
import re
from math import log

def parse_result_file(filename):
    data = []
    with open(filename, 'r') as file:
        for line in file:
            # Extract matrix name, time, memory, vertices, and edges
            match = re.match(r'(.*): ([\d.]+) seconds, Memory : (\d+) Bytes, Integers: (\d+), (\d+)', line)
            if match:
                matrix, time, memory, vertices, edges = match.groups()
                data.append({
                    'matrix': matrix.strip(),
                    'time': float(time),
                    'memory': int(memory),
                    'vertices': int(vertices),
                    'edges': int(edges),
                    'density': int(edges) / (int(vertices) * int(vertices))  # Calculate density
                })
    return data

def classify_graphs(data, density_threshold=0.005):
    """Classify graphs as sparse or dense based on edge density threshold."""
    sparse = [item for item in data if item['density'] < density_threshold]
    dense = [item for item in data if item['density'] >= density_threshold]
    return sparse, dense

def plot_comparative_time_analysis(slota_data, Tarjan_data):
    """Plot time analysis comparing both algorithms for sparse and dense graphs."""
    # Classify graphs as sparse or dense for both algorithms
    sparse_slota, dense_slota = classify_graphs(slota_data)
    sparse_Tarjan, dense_Tarjan = classify_graphs(Tarjan_data)

    # Sort by number of edges
    sparse_slota.sort(key=lambda x: x['edges'])
    dense_slota.sort(key=lambda x: x['edges'])
    sparse_Tarjan.sort(key=lambda x: x['edges'])
    dense_Tarjan.sort(key=lambda x: x['edges'])

    # Create figure with two subplots (sparse vs dense)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    fig.suptitle('Time Analysis: Slota vs Tarjan Algorithm', fontsize=16)

    # Sparse graphs subplot
    edges_sparse_slota = [item['edges'] for item in sparse_slota]
    times_sparse_slota = [item['time'] for item in sparse_slota]
    edges_sparse_Tarjan = [item['edges'] for item in sparse_Tarjan]
    times_sparse_Tarjan = [item['time'] for item in sparse_Tarjan]

    # Plot time vs edges for sparse graphs
    ax1.plot(edges_sparse_slota, times_sparse_slota, 'b-', marker='o', markersize=4, alpha=0.7, label='Slota')
    ax1.plot(edges_sparse_Tarjan, times_sparse_Tarjan, 'r-', marker='s', markersize=4, alpha=0.7, label='Tarjan')
    ax1.set_xlabel('Number of Edges')
    ax1.set_ylabel('Time (seconds)')
    ax1.set_title(f'Sparse Graphs (Slota n={len(sparse_slota)}, Tarjan n={len(sparse_Tarjan)})')
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.legend()

    # Set log scales for better visualization
    ax1.set_xscale('log')
    ax1.set_yscale('log')

    # Dense graphs subplot
    edges_dense_slota = [item['edges'] for item in dense_slota]
    times_dense_slota = [item['time'] for item in dense_slota]
    edges_dense_Tarjan = [item['edges'] for item in dense_Tarjan]
    times_dense_Tarjan = [item['time'] for item in dense_Tarjan]

    # Plot time vs edges for dense graphs
    ax2.plot(edges_dense_slota, times_dense_slota, 'b-', marker='o', markersize=4, alpha=0.7, label='Slota')
    ax2.plot(edges_dense_Tarjan, times_dense_Tarjan, 'r-', marker='s', markersize=4, alpha=0.7, label='Tarjan')
    ax2.set_xlabel('Number of Edges')
    ax2.set_ylabel('Time (seconds)')
    ax2.set_title(f'Dense Graphs (Slota n={len(dense_slota)}, Tarjan n={len(dense_Tarjan)})')
    ax2.grid(True, linestyle='--', alpha=0.7)
    ax2.legend()

    # Set log scales for better visualization
    ax2.set_xscale('log')
    ax2.set_yscale('log')

    plt.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust to make room for the title
    return fig

def plot_comparative_memory_analysis(slota_data, Tarjan_data):
    """Plot memory analysis comparing both algorithms for sparse and dense graphs."""
    # Classify graphs as sparse or dense for both algorithms
    sparse_slota, dense_slota = classify_graphs(slota_data)
    sparse_Tarjan, dense_Tarjan = classify_graphs(Tarjan_data)

    # Sort by number of edges
    sparse_slota.sort(key=lambda x: x['edges'])
    dense_slota.sort(key=lambda x: x['edges'])
    sparse_Tarjan.sort(key=lambda x: x['edges'])
    dense_Tarjan.sort(key=lambda x: x['edges'])

    # Create figure with two subplots (sparse vs dense)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    fig.suptitle('Memory Analysis: Slota vs Tarjan Algorithm', fontsize=16)

    # Sparse graphs subplot
    edges_sparse_slota = [item['edges'] for item in sparse_slota]
    memory_sparse_slota = [item['memory'] / (1024 * 1024) for item in sparse_slota]  # Convert to MB
    edges_sparse_Tarjan = [item['edges'] for item in sparse_Tarjan]
    memory_sparse_Tarjan = [item['memory'] / (1024 * 1024) for item in sparse_Tarjan]  # Convert to MB

    # Plot memory vs edges for sparse graphs
    ax1.plot(edges_sparse_slota, memory_sparse_slota, 'b-', marker='o', markersize=4, alpha=0.7, label='Slota')
    ax1.plot(edges_sparse_Tarjan, memory_sparse_Tarjan, 'r-', marker='s', markersize=4, alpha=0.7, label='Tarjan')
    ax1.set_xlabel('Number of Edges')
    ax1.set_ylabel('Memory (MB)')
    ax1.set_title(f'Sparse Graphs (Slota n={len(sparse_slota)}, Tarjan n={len(sparse_Tarjan)})')
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.legend()

    # Set log scales for better visualization
    ax1.set_xscale('log')
    ax1.set_yscale('log')

    # Dense graphs subplot
    edges_dense_slota = [item['edges'] for item in dense_slota]
    memory_dense_slota = [item['memory'] / (1024 * 1024) for item in dense_slota]  # Convert to MB
    edges_dense_Tarjan = [item['edges'] for item in dense_Tarjan]
    memory_dense_Tarjan = [item['memory'] / (1024 * 1024) for item in dense_Tarjan]  # Convert to MB

    # Plot memory vs edges for dense graphs
    ax2.plot(edges_dense_slota, memory_dense_slota, 'b-', marker='o', markersize=4, alpha=0.7, label='Slota')
    ax2.plot(edges_dense_Tarjan, memory_dense_Tarjan, 'r-', marker='s', markersize=4, alpha=0.7, label='Tarjan')
    ax2.set_xlabel('Number of Edges')
    ax2.set_ylabel('Memory (MB)')
    ax2.set_title(f'Dense Graphs (Slota n={len(dense_slota)}, Tarjan n={len(dense_Tarjan)})')
    ax2.grid(True, linestyle='--', alpha=0.7)
    ax2.legend()

    # Set log scales for better visualization
    ax2.set_xscale('log')
    ax2.set_yscale('log')

    plt.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust to make room for the title
    return fig

def plot_double_bar_comparison(slota_data, Tarjan_data, metric='time', graph_type='sparse'):
    """Plot a double bar comparison (time or memory) for Slota vs Tarjan algorithms."""
    # Classify graphs as sparse or dense
    sparse_slota, dense_slota = classify_graphs(slota_data)
    sparse_Tarjan, dense_Tarjan = classify_graphs(Tarjan_data)

    if graph_type == 'sparse':
        slota = sparse_slota
        Tarjan = sparse_Tarjan
        title_suffix = 'Sparse Graphs'
    else:
        slota = dense_slota
        Tarjan = dense_Tarjan
        title_suffix = 'Dense Graphs'

    # Sort by number of edges to keep order consistent
    slota.sort(key=lambda x: x['edges'])
    Tarjan.sort(key=lambda x: x['edges'])

    labels = [item['matrix'] for item in slota]
    edges = [item['edges'] for item in slota]

    if metric == 'time':
        slota_values = [item['time'] for item in slota]
        Tarjan_values = [item['time'] for item in Tarjan]
        ylabel = 'Time (seconds)'
    else:
        slota_values = [item['memory'] / (1024 * 1024) for item in slota]  # Convert to MB
        Tarjan_values = [item['memory'] / (1024 * 1024) for item in Tarjan]
        ylabel = 'Memory (MB)'

    x = np.arange(len(labels))  # the label locations
    width = 0.4  # width of the bars

    fig, ax = plt.subplots(figsize=(16, 8))
    ax.set_title(f'{metric.capitalize()} Comparison: Slota vs Tarjan ({title_suffix})', fontsize=16)

    # Determine front and back bar ordering dynamically (smaller in front)
    for i in range(len(x)):
        if slota_values[i] <= Tarjan_values[i]:
            ax.bar(x[i], log(Tarjan_values[i]), width, label='Tarjan' if i==0 else "", color='red', alpha=0.4, zorder=1)
            ax.bar(x[i], log(slota_values[i]), width*0.7, label='Slota' if i==0 else "", color='blue', alpha=0.9, zorder=2)
        else:
            ax.bar(x[i], log(slota_values[i]), width, label='Slota' if i==0 else "", color='blue', alpha=0.4, zorder=1)
            ax.bar(x[i], log(Tarjan_values[i]), width*0.7, label='Tarjan' if i==0 else "", color='red', alpha=0.9, zorder=2)

    ax.set_xlabel('Graph Dataset')
    ax.set_ylabel(ylabel)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha='right')
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.5, axis='y')

    plt.tight_layout()
    return fig


def main():
    # Parse data
    slota_data = parse_result_file('slota_result1.txt')
    Tarjan_data = parse_result_file('tarjan_result1.txt')

    # Print statistics
    sparse_slota, dense_slota = classify_graphs(slota_data)
    sparse_Tarjan, dense_Tarjan = classify_graphs(Tarjan_data)

    print(f"Total matrices: {len(slota_data)}")
    print(f"Slota - Sparse matrices: {len(sparse_slota)}, Dense matrices: {len(dense_slota)}")
    print(f"Tarjan - Sparse matrices: {len(sparse_Tarjan)}, Dense matrices: {len(dense_Tarjan)}")

    # Create comparative analysis plots
    time_comparison_fig = plot_comparative_time_analysis(slota_data, Tarjan_data)
    time_comparison_fig.savefig('time_comparison_21.png', dpi=300, bbox_inches='tight')

    memory_comparison_fig = plot_comparative_memory_analysis(slota_data, Tarjan_data)
    memory_comparison_fig.savefig('memory_comparison_21.png', dpi=300, bbox_inches='tight')

    # Calculate and print performance statistics
    print("\nPerformance Summary:")
    print("-------------------")

    # Calculate average performance for each algorithm and graph type
    avg_time_slota_sparse = sum(item['time'] for item in sparse_slota) / len(sparse_slota) if sparse_slota else 0
    avg_time_slota_dense = sum(item['time'] for item in dense_slota) / len(dense_slota) if dense_slota else 0
    avg_time_Tarjan_sparse = sum(item['time'] for item in sparse_Tarjan) / len(sparse_Tarjan) if sparse_Tarjan else 0
    avg_time_Tarjan_dense = sum(item['time'] for item in dense_Tarjan) / len(dense_Tarjan) if dense_Tarjan else 0

    avg_memory_slota_sparse = sum(item['memory'] for item in sparse_slota) / len(sparse_slota) / (1024 * 1024) if sparse_slota else 0  # Convert to MB
    avg_memory_slota_dense = sum(item['memory'] for item in dense_slota) / len(dense_slota) / (1024 * 1024) if dense_slota else 0
    avg_memory_Tarjan_sparse = sum(item['memory'] for item in sparse_Tarjan) / len(sparse_Tarjan) / (1024 * 1024) if sparse_Tarjan else 0
    avg_memory_Tarjan_dense = sum(item['memory'] for item in dense_Tarjan) / len(dense_Tarjan) / (1024 * 1024) if dense_Tarjan else 0

    print(f"Slota - Avg Time (Sparse): {avg_time_slota_sparse:.4f} seconds, Avg Time (Dense): {avg_time_slota_dense:.4f} seconds")
    print(f"Tarjan - Avg Time (Sparse): {avg_time_Tarjan_sparse:.4f} seconds, Avg Time (Dense): {avg_time_Tarjan_dense:.4f} seconds")
    print(f"Slota - Avg Memory (Sparse): {avg_memory_slota_sparse:.2f} MB, Avg Memory (Dense): {avg_memory_slota_dense:.2f} MB")
    print(f"Tarjan - Avg Memory (Sparse): {avg_memory_Tarjan_sparse:.2f} MB, Avg Memory (Dense): {avg_memory_Tarjan_dense:.2f} MB")

    # Calculate relative performance (Tarjan/Slota)
    print("\nRelative Performance (Tarjan/Slota):")
    print(f"Time Ratio (Sparse): {avg_time_Tarjan_sparse/avg_time_slota_sparse:.2f}x" if avg_time_slota_sparse > 0 else "N/A")
    print(f"Time Ratio (Dense): {avg_time_Tarjan_dense/avg_time_slota_dense:.2f}x" if avg_time_slota_dense > 0 else "N/A")
    print(f"Memory Ratio (Sparse): {avg_memory_Tarjan_sparse/avg_memory_slota_sparse:.2f}x" if avg_memory_slota_sparse > 0 else "N/A")
    print(f"Memory Ratio (Dense): {avg_memory_Tarjan_dense/avg_memory_slota_dense:.2f}x" if avg_memory_slota_dense > 0 else "N/A")

    # Calculate median performance statistics
    def get_median(values):
        sorted_values = sorted(values)
        mid = len(sorted_values) // 2
        if len(sorted_values) % 2 == 0:
            return (sorted_values[mid-1] + sorted_values[mid]) / 2
        else:
            return sorted_values[mid]

    print("\nMedian Performance:")
    median_time_slota_sparse = get_median([item['time'] for item in sparse_slota]) if sparse_slota else 0
    median_time_slota_dense = get_median([item['time'] for item in dense_slota]) if dense_slota else 0
    median_time_Tarjan_sparse = get_median([item['time'] for item in sparse_Tarjan]) if sparse_Tarjan else 0
    median_time_Tarjan_dense = get_median([item['time'] for item in dense_Tarjan]) if dense_Tarjan else 0

    median_memory_slota_sparse = get_median([item['memory'] for item in sparse_slota]) / (1024 * 1024) if sparse_slota else 0
    median_memory_slota_dense = get_median([item['memory'] for item in dense_slota]) / (1024 * 1024) if dense_slota else 0
    median_memory_Tarjan_sparse = get_median([item['memory'] for item in sparse_Tarjan]) / (1024 * 1024) if sparse_Tarjan else 0
    median_memory_Tarjan_dense = get_median([item['memory'] for item in dense_Tarjan]) / (1024 * 1024) if dense_Tarjan else 0

    print(f"Slota - Median Time (Sparse): {median_time_slota_sparse:.4f} seconds, Median Time (Dense): {median_time_slota_dense:.4f} seconds")
    print(f"Tarjan - Median Time (Sparse): {median_time_Tarjan_sparse:.4f} seconds, Median Time (Dense): {median_time_Tarjan_dense:.4f} seconds")
    print(f"Slota - Median Memory (Sparse): {median_memory_slota_sparse:.2f} MB, Median Memory (Dense): {median_memory_slota_dense:.2f} MB")
    print(f"Tarjan - Median Memory (Sparse): {median_memory_Tarjan_sparse:.2f} MB, Median Memory (Dense): {median_memory_Tarjan_dense:.2f} MB")

    fig_time_sparse = plot_double_bar_comparison(slota_data, Tarjan_data, metric='time', graph_type='sparse')
    fig_time_sparse.savefig('double_bar_time_sparse.png', dpi=300, bbox_inches='tight')
    
    fig_time_sparse = plot_double_bar_comparison(slota_data, Tarjan_data, metric='time', graph_type='dense')
    fig_time_sparse.savefig('double_bar_time_dense.png', dpi=300, bbox_inches='tight')
    
    fig_mem_dense = plot_double_bar_comparison(slota_data, Tarjan_data, metric='memory', graph_type='sparse')
    fig_mem_dense.savefig('double_bar_memory_sparse.png', dpi=300, bbox_inches='tight')

    fig_mem_dense = plot_double_bar_comparison(slota_data, Tarjan_data, metric='memory', graph_type='dense')
    fig_mem_dense.savefig('double_bar_memory_dense.png', dpi=300, bbox_inches='tight')


if __name__ == "__main__":
    main()