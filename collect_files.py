import os
import shutil
import argparse


def copy_file(filepath: str, output_dir: str):
    filename = os.path.basename(filepath)
    if not os.path.exists(os.path.join(output_dir, filename)):
        shutil.copy(filepath, output_dir)
        return
    else:
        suffix = 1
        base, extension = os.path.splitext(filename)
        while True:
            new_filename = f"{base}{suffix}{extension}"
            if os.path.exists(os.path.join(output_dir, new_filename)):
                suffix += 1
                continue
            else:
                shutil.copy(filepath, os.path.join(output_dir, new_filename))
                break


def collect_files(input_dir: str, output_dir: str, depth: int = -1):
    for p in os.listdir(input_dir):
        path = os.path.join(input_dir, p)
        if os.path.isfile(path):
            copy_file(path, output_dir)
        elif os.path.isdir(path):
            if depth == -1:
                collect_files(path, output_dir)
            elif depth > 1:
                collect_files(path, output_dir, depth-1)


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

    collect_files(args.input_dir, args.output_dir, args.max_depth)


if __name__ == "__main__":
    main()
