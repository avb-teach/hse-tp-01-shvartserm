import os
import shutil
import argparse


def gen_filename(output_dir: str, relative_path: list[str], filename: str):
    if not os.path.exists(os.path.join(output_dir, *relative_path, filename)):
        return filename
    
    suffix = 1
    base, extension = os.path.splitext(filename)
    while True:
        new_filename = f"{base}{suffix}{extension}"
        if os.path.exists(os.path.join(output_dir, *relative_path, new_filename)):
            suffix += 1
            continue
        else:
            return new_filename


def copy_file(filepath: str, relative_path: list[str], output_dir: str, max_depth: int):
    filename = os.path.basename(filepath)

    if max_depth in [-1, 1]:
        relative_path = []
    else:
        relative_path = relative_path[-(max_depth-1):]
    
    os.makedirs(os.path.join(output_dir, *relative_path), exist_ok=True)
    filename = gen_filename(output_dir, relative_path, filename)
    shutil.copy(filepath, os.path.join(output_dir, *relative_path, filename))


def collect_files(input_dir: str, output_dir: str, relative_path: list[str] = [], max_depth: int = -1):
    for p in os.listdir(input_dir):
        path = os.path.join(input_dir, p)
        if os.path.isfile(path):
            copy_file(path, relative_path, output_dir, max_depth)
        elif os.path.isdir(path):
            collect_files(path, output_dir, relative_path + [os.path.basename(path)], max_depth)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", type=str)
    parser.add_argument("output_dir", type=str)
    parser.add_argument("--max_depth", type=int, default=-1)

    args = parser.parse_args()

    if not os.path.exists(args.input_dir) or not os.path.isdir(args.input_dir):
        print("ERROR: input_dir must be an existing directory")
        return

    if not os.path.exists(args.output_dir) or not os.path.isdir(args.output_dir):
        print("ERROR: output_dir must be an existing directory")
        return

    collect_files(args.input_dir, args.output_dir, [], args.max_depth)


if __name__ == "__main__":
    main()
