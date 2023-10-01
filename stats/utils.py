import glob
from pathlib import PurePath, Path

def dir_path():
    output_root = 'output/report_output'
    directories = []
    # The pattern '**' matches any files or directories (including those starting with '.')
    # The pattern '*/' matches any directory
    for dir in glob.glob(f"{output_root}/*/*/"):
        dir_path = Path(dir)
        directories.append(dir_path)

    return directories

def main():
    dir_path()

if __name__ == "__main__":
    main()
