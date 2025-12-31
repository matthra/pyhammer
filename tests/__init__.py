"""
PyHammer test suite.

This __init__.py ensures proper import paths for all test files.
"""

import sys
import os

# Add parent directory to path so 'src' imports work
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
