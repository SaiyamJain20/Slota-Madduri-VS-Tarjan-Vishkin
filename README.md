
# Graph Analysis Program

This is a comparison between two different algorithms which are both used to find Biconnnected components of a graph.

## Requirements

* A C++ compiler (C++11 or later)
* Linux-based OS (for `sys/resource.h`)

## Compilation

### To run Slota Algorith

1. Compile the program:

   ```bash
   g++ slota.cpp -o slota
   ```

2. Run the program:
   
   ```bash
   ./slota
    ```

### To run Tarjan-Vishkin Algorithm

1. Compile the program:

   ```bash
   g++ tarjan.cpp -o tarjan
   ```

2. Run the program:
   
   ```bash
   ./tarjan
    ```
   

## Input File Format in file named `graph.txt`

The program expects a graph file with the following format:

```
n n m
u1 v1 weight1
u2 v2 weight2
...
```

Where `n` is the number of nodes, `m` is the number of edges, and each edge is represented by two nodes and a weight.

## Output

It prints the number of vertices `n` followed by number of edges `m` and finally memory taken by it.

## Extra files

In the Scripts we have included files using which we have gotten the final outputs

### `script.py`

Require change to

```
cpp_file1 = "/home/saiyamjain/Desktop/AlgoEngg/Project/tarjan.cpp"
cpp_file2 = "/home/saiyamjain/Desktop/AlgoEngg/Project/slota.cpp"
input_dir = "/home/saiyamjain/Desktop/AlgoEngg/Project/matrices"
output_txt1 = "/home/saiyamjain/Desktop/AlgoEngg/Project/tarjan_result.txt"
output_txt2 = "/home/saiyamjain/Desktop/AlgoEngg/Project/slota_result.txt"
```

To your laptops location, other than that directly run using python