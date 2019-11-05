import math
import os
import json

from . import config_base

def get_substitution_list():
    substitution_list = []
    for index in [energy for energy in range(3, 31, 3)]: #range(30, 31, 3)]:
        sub = config_base.get_baseline_substitution()
        sub["__energy__"] = float(index)
        substitution_list.append(sub)
    print(json.dumps(substitution_list, indent=2))
    return substitution_list

class Config(config_base.Config):
    def __init__(self):
        super(Config, self).__init__()
        self.run_control["output_dir"] = os.path.join(os.getcwd(), "output/baseline_energy_scan")
        self.substitution_list = get_substitution_list()
        self.run_control["find_closed_orbits"] = True
        self.run_control["find_tune"] = False
        self.run_control["find_da"] = False
