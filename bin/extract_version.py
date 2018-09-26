"""
Script that extracts a version from a Python
__version__ variable and prints it to
standard output.
"""
import os
import sys

repository_directory = os.path.dirname(os.path.realpath(__file__)).replace('bin', '')
sys.path.append(repository_directory)

from skill.metadata import __version__
print(__version__)