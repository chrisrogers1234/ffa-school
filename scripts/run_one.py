import os
import shutil
import sys
import importlib

import xboa.common

import find_closed_orbits
import find_tune
import find_da

def get_config():
    config_file = sys.argv[1].replace(".py", "")
    config_file = config_file.split("scripts/")[1]
    config_file = config_file.replace("/", ".")
    print "Using configuration module", config_file
    config_mod = importlib.import_module(config_file)
    config = config_mod.Config()
    return config

def output_dir(config):
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

def master_substitutions(config):
    xboa.common.substitute(config.tracking["master_file"], config.tracking["lattice_file"], config.master_substitutions)

def main():
    config = get_config()
    output_dir(config)
    #master_substitutions(config)
    if config.run_control["find_closed_orbits"]:
        find_closed_orbits.main(config)
    if config.run_control["find_tune"]:
        find_tune.main(config)
    if config.run_control["find_da"]:
        find_da.main(config)
    
if __name__ == "__main__":
    main()
