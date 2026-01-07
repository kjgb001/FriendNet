#!/usr/bin/env python3

from cli.cli import main
from utils.logger import setup_logging
'''
import faulthandler
faulthandler.enable(all_threads=True)
# DEBUG
'''

setup_logging()

if __name__ == "__main__":
    main()
