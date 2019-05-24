import math
import os
import json

import config_base

def get_substitution_list():
    substitution_list = []
    for index in [energy for energy in range(3, 31, 3)]: #range(30, 31, 3)]:
        sub = config_base.get_baseline_substitution()
        sub["__energy__"] = float(index)
        sub["__tan_delta__"] = -math.tan(math.radians(41))
        sub["__beam_phi_init__"] = 0.0
        sub["__lattice_phi_offset__"] = 0.15
        sub["__step_size__"] = 1.0
        substitution_list.append(sub)
    print json.dumps(substitution_list, indent=2)
    return substitution_list

class Config(config_base.Config):
    def __init__(self):
        super(Config, self).__init__()
        self.run_control["output_dir"] = os.path.join(os.getcwd(), "output/baseline_energy_scan_2")
        self.substitution_list = get_substitution_list()
        self.run_control["find_closed_orbits"] = False
        self.run_control["find_tune"] = True
        self.find_tune["subs_overrides"]["__n_turns__"] = 10.1
        self.find_tune["probe_files"] = "RINGPROBE*.loss"
        self.find_closed_orbits["seed"] = [[4042.16, -8.4729,]] # 3 MeV
        #self.find_closed_orbits["seed"] = [[4741.62, 5.3204,]] # 30 MeV
        #self.find_closed_orbits["seed"] = [[4673.02693036, -31.46921736]] # 30 MeV
