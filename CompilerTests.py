import os
import glob
from CompilerProgram import execute_file


def run_compiler_tests():
    test_files_dir = "test_files"
    # Find all files in the "test_files" directory.
    input_files = glob.glob(os.path.join(test_files_dir, "*"))

    if not input_files:
        print(f"No input files found in {test_files_dir}")
        return

    for input_file in input_files:
        print(f"Running compiler on: {input_file}")
        execute_file(input_file)


if __name__ == "__main__":
    run_compiler_tests()
