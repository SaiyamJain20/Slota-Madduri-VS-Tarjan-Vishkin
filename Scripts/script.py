import subprocess
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def compile_cpp_code(cpp_file, executable_name):
    """Compile the C++ code using g++."""
    compile_command = ["g++", cpp_file, "-o", executable_name]
    try:
        subprocess.run(compile_command, check=True)
        print(f"Compilation of {cpp_file} successful.")
    except subprocess.CalledProcessError:
        print(f"Compilation of {cpp_file} failed.")
        exit(1)

def run_cpp_with_input_file(executable, input_file):
    """Run the compiled executable with a given .mtx input file and return the time taken and output."""
    start_time = time.time()
    try:
        result = subprocess.run(
            [f"./{executable}", input_file], check=True, capture_output=True, text=True
        )
        output = result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running {input_file}: {e.stderr}")
        return input_file, None, None
    
    end_time = time.time()

    output_lines = output.strip().split("\n")
    if output_lines:
        try:
            integers = list(map(int, output_lines[-1].split()))
            if len(integers) == 3:
                return input_file, end_time - start_time, integers
            else:
                print(f"Unexpected output format in {input_file}. Expected 3 integers.")
        except ValueError:
            print(f"Could not parse integers from output of {input_file}.")
    
    return input_file, None, None

def process_files_concurrent(executable, input_dir, output_txt, max_workers=8):
    """Process each .mtx file concurrently using threads."""
    futures = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for filename in os.listdir(input_dir):
            if filename.endswith(".mtx"):
                input_file = os.path.join(input_dir, filename)
                print(f"Submitting {input_file}...")
                futures.append(executor.submit(run_cpp_with_input_file, executable, input_file))
        
        with open(output_txt, "a") as output_file:
            for future in as_completed(futures):
                input_file, time_taken, integers = future.result()
                if time_taken is not None and integers is not None:
                    filename = os.path.basename(input_file)
                    output_file.write(
                        f"{filename}: {time_taken:.6f} seconds, Memory : {integers[2]} Bytes, Integers: {integers[0]}, {integers[1]}\n"
                    )
                    print(f"{filename}: {time_taken:.6f}s, Mem: {integers[2]} Bytes, Ints: {integers[0]}, {integers[1]}")
                else:
                    print(f"Failed to process {input_file}")
            output_file.write("\n")

    print(f"Results saved to {output_txt}")

def main():
    cpp_file1 = "/home/saiyamjain/Desktop/AlgoEngg/Project/tarjan.cpp"
    cpp_file2 = "/home/saiyamjain/Desktop/AlgoEngg/Project/slota.cpp"
    input_dir = "/home/saiyamjain/Desktop/AlgoEngg/Project/matrices"
    output_txt1 = "/home/saiyamjain/Desktop/AlgoEngg/Project/tarjan_result.txt"
    output_txt2 = "/home/saiyamjain/Desktop/AlgoEngg/Project/slota_result.txt"
    
    executable1 = "executable1"
    executable2 = "executable2"

    compile_cpp_code(cpp_file1, executable1)
    process_files_concurrent(executable1, input_dir, output_txt1)

    compile_cpp_code(cpp_file2, executable2)
    process_files_concurrent(executable2, input_dir, output_txt2)

if __name__ == "__main__":
    main()
