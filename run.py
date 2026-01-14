#!/usr/bin/env python3

import sys
import importlib.util
from cli.cli import main
from utils.logger import setup_logging

REQUIRED_PACKAGES = [
    "networkx",
    "matplotlib",
    "PySide6",
    "pytest"
]


def check_python_version():
    if sys.version_info < (3, 10):
        print("❌ Python 3.10+ is required.")
        sys.exit(1)


def check_dependencies():
    missing = [
        pkg for pkg in REQUIRED_PACKAGES
        if importlib.util.find_spec(pkg) is None
    ]

    if missing:
        print("❌ Missing required package(s):")
        for pkg in missing:
            print(f"  - {pkg}")
        print("\nInstall them with:")
        print(f"  pip install {' '.join(missing)}")
        sys.exit(1)


def launch():
    main()


if __name__ == "__main__":
    check_python_version()
    check_dependencies()
    setup_logging()
    launch()
