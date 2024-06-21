import os
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

def copy_file(file_path, target_dir):
    ext = file_path.suffix[1:]
    target_folder = target_dir / ext

    if not target_folder.exists():
        target_folder.mkdir(parents=True, exist_ok=True)

    shutil.copy(file_path, target_folder / file_path.name)

def process_directory(directory, target_dir):
    futures = []
    with ThreadPoolExecutor() as executor:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = Path(root) / file
                futures.append(executor.submit(copy_file, file_path, target_dir))

        for future in as_completed(futures):
            future.result()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python script.py <source_directory> [<target_directory>]")
        sys.exit(1)

    source_directory = Path(sys.argv[1])
    target_directory = Path(sys.argv[2]) if len(sys.argv) > 2 else Path('dist')

    if not source_directory.exists() or not source_directory.is_dir():
        print(f"Source directory '{source_directory}' does not exist or is not a directory.")
        sys.exit(1)

    if not target_directory.exists():
        target_directory.mkdir(parents=True, exist_ok=True)

    process_directory(source_directory, target_directory)
    print("Files copied and sorted successfully.")