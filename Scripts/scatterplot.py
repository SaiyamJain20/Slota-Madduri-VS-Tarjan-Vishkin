import matplotlib.pyplot as plt
import numpy as np
import re

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
    ax1.scatter(edges_sparse_slota, times_sparse_slota, color='blue', label='Slota', alpha=0.7)
    ax1.scatter(edges_sparse_Tarjan, times_sparse_Tarjan, color='red', label='Tarjan', alpha=0.7)
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
    ax2.scatter(edges_dense_slota, times_dense_slota, color='blue', label='Slota', alpha=0.7)
    ax2.scatter(edges_dense_Tarjan, times_dense_Tarjan, color='red', label='Tarjan', alpha=0.7)
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
    ax1.scatter(edges_sparse_slota, memory_sparse_slota, color='blue', label='Slota', alpha=0.7)
    ax1.scatter(edges_sparse_Tarjan, memory_sparse_Tarjan, color='red', label='Tarjan', alpha=0.7)
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
    ax2.scatter(edges_dense_slota, memory_dense_slota, color='blue', label='Slota', alpha=0.7)
    ax2.scatter(edges_dense_Tarjan, memory_dense_Tarjan, color='red', label='Tarjan', alpha=0.7)
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

def main():
    # Parse data
    slota_data = parse_result_file('slota_result.txt')
    Tarjan_data = parse_result_file('tarjan_result.txt')

    # Print statistics
    sparse_slota, dense_slota = classify_graphs(slota_data)
    sparse_Tarjan, dense_Tarjan = classify_graphs(Tarjan_data)

    print(f"Total matrices: {len(slota_data)}")
    print(f"Slota - Sparse matrices: {len(sparse_slota)}, Dense matrices: {len(dense_slota)}")
    print(f"Tarjan - Sparse matrices: {len(sparse_Tarjan)}, Dense matrices: {len(dense_Tarjan)}")

    # Create comparative analysis plots
    time_comparison_fig = plot_comparative_time_analysis(slota_data, Tarjan_data)
    time_comparison_fig.savefig('time_comparison_scatter2.png', dpi=300, bbox_inches='tight')

    memory_comparison_fig = plot_comparative_memory_analysis(slota_data, Tarjan_data)
    memory_comparison_fig.savefig('memory_comparison_scatter2.png', dpi=300, bbox_inches='tight')

    # Further code to generate bar charts, performance statistics, etc.

if __name__ == "__main__":
    main()
