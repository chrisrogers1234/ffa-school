import os
import config_base

class Config(config_base.Config):
    pass

Config.run_control = {
        "find_closed_orbits":False,
        "find_tune":False,
        "find_da":False,
        "track_beam":True,
        "clean_output_dir":False,
        "output_dir":os.path.join(os.getcwd(), "output/baseline_alt"),
    }

