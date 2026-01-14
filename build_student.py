#!/usr/bin/env python3

import shutil
from pathlib import Path

ROOT = Path(__file__).parent
STUDENT_DIR = ROOT / "student"

INCLUDE = [
    "cli",
    "core",
    "utils",
    "view",
    "assets",
    "run.py",
    "README.md",
    "LICENSE",
    "requirements.txt",
]

EXCLUDE_PATTERNS = [
    "__pycache__",
    "*.log",
    "*.tmp",
]

STUDENT_README = ROOT / "docs" / "README_student.md"


def clean_student_dir():
    if STUDENT_DIR.exists():
        print("Removing existing student directory")
        shutil.rmtree(STUDENT_DIR)
    STUDENT_DIR.mkdir()


def copy_item(name):
    src = ROOT / name
    dst = STUDENT_DIR / name

    if not src.exists():
        return

    if src.is_dir():
        shutil.copytree(
            src,
            dst,
            ignore=shutil.ignore_patterns(*EXCLUDE_PATTERNS),
        )
    else:
        shutil.copy2(src, dst)


def remove_matrix_graph():
    matrix_graph = STUDENT_DIR / "core" / "matrixGraph.py"
    if matrix_graph.exists():
        matrix_graph.unlink()
        print("Removed core/matrixGraph.py from student build")


def clear_asset_subdirs():
    asset_dirs = [
        STUDENT_DIR / "assets" / "people",
        STUDENT_DIR / "assets" / "portraits",
    ]

    for path in asset_dirs:
        if path.exists():
            clear_directory_contents(path)
            print(f"Cleared contents of {path.relative_to(STUDENT_DIR)}")

def clear_directory_contents(path):
    if not path.exists() or not path.is_dir():
        return

    for item in path.iterdir():
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()


def copy_student_readme():
    if not STUDENT_README.exists():
        raise FileNotFoundError("docs/README_student.md not found")

    shutil.copy2(STUDENT_README, STUDENT_DIR / "README.md")


def clean_requirements():
    req_path = STUDENT_DIR / "requirements.txt"
    if not req_path.exists():
        return

    lines = req_path.read_text().splitlines()
    cleaned = [line for line in lines if line.strip() != "pytest"]

    req_path.write_text("\n".join(cleaned) + "\n")
    print("Removed pytest from requirements.txt")



def main():
    print("\nBuilding student-facing copy...")
    clean_student_dir()

    for item in INCLUDE:
        copy_item(item)

    remove_matrix_graph()
    clear_asset_subdirs()
    copy_student_readme()
    clean_requirements()

    print(f"Student build ready at: {STUDENT_DIR}/\n")


if __name__ == "__main__":
    main()
