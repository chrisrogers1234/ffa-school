import math
import os
import config_base

DIR = "fixed_frequency_rf"


def get_substitution_list():
    energy_list = [range(3, 5, 1)]
    substitution_list = [config_base.get_baseline_substitution()]

class Config(config_base.Config):
    def __init__(self):
        super(Config, self).__init__()
        self.run_control = {
            "find_closed_orbits":True,
            "find_tune":False,
            "find_da":False,
            "find_rf_parameters":False,
            "find_bump_parameters":False,
            "track_beam":False,
            "track_bump":False,
            "clean_output_dir":False,
            "output_dir":os.path.join(os.getcwd(), "output/"+DIR),
        }
        self.find_closed_orbits = {
            "seed":[[4042.10640218, -8.47136893],],
            "output_file":"find_closed_orbit",
            "subs_overrides":{"__n_turns__":1.1, "__no_field_maps__":""},
            "root_batch":0,
            "max_iterations":10,
            "do_plot_orbit":False,
            "run_dir":"tmp/find_closed_orbits/",
            "probe_files":"RINGPROBE*.loss",
        }


