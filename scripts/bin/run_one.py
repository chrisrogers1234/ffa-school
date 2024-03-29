"""
This program runs the various subroutines for the FFA school
"""

import os
import shutil
import sys
import importlib

import xboa.common

import analysis.find_closed_orbits
import analysis.find_tune
import analysis.find_da
from utils import utilities

def get_config():
    """
    Load a configuration file specified on the command line
    """
    if len(sys.argv) < 2:
        print("Usage: python /path/to/run_one.py /path/to/config.py")
        sys.exit(1)
    config_file = sys.argv[1].replace(".py", "")
    config_file = config_file.split("scripts/")[1]
    config_file = config_file.replace("/", ".")
    print("Using configuration module", config_file)
    config_mod = importlib.import_module(config_file)
    config = config_mod.Config()
    return config

def output_dir(config):
    """
    Setup the output directory
    - if run_control["clean_output_dir"] is set to true, delete the existing
      directory first
    """
    output_dir = config.run_control["output_dir"]
    if config.run_control["clean_output_dir"]:
        try:
            shutil.rmtree(output_dir)
        except OSError:
            pass
    try:
        os.makedirs(output_dir)
    except OSError:
        pass

def main():
    """
    The main program loop
    """
    config = get_config()
    output_dir(config)
    if config.run_control["find_closed_orbits"]:
        analysis.find_closed_orbits.main(config)
    if config.run_control["find_tune"]:
        analysis.find_tune.main(config)
    if config.run_control["find_da"]:
        analysis.find_da.main(config)

if __name__ == "__main__":
    main()
