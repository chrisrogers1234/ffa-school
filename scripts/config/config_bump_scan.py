import copy
import os
import json

import config_bump as config
DIR = config.DIR

# 0.21625, 0.21833
def get_substitution_list():
    str_in = open("output/"+DIR+"/find_bump_parameters.tmp").read()
    json_in = json.loads(str_in)
    subs_list = []
    for item in json_in:
        subs = item["subs"]
        for bump in item["bumps"]:
            for i, bump_field in enumerate(bump["bump_fields"]):
                subs["__bump_field_"+str(i+1)+"__"] = bump_field
            subs_list.append(copy.deepcopy(subs))
    return subs_list

class Config(config.Config):
    def __init__(self):
        super(Config, self).__init__()
        self.run_control = {
            "find_closed_orbits":True,
            "find_tune":True,
            "find_da":True,
            "find_rf_parameters":False,
            "find_bump_parameters":False,
            "track_beam":False,
            "track_bump":False,
            "clean_output_dir":False,
            "output_dir":os.path.join(os.getcwd(), "output/"+DIR),
        }
        self.find_closed_orbits["subs_overrides"]["__n_turns__"] = 10
        self.find_closed_orbits["probe_files"] = "RINGPROBE01.loss"
        self.find_tune["subs_overrides"]["__n_turns__"] = 50
        self.find_tune["probe_files"] = "FOILPROBE.loss"
        self.find_da["max_iterations"] = 20
        self.find_da["probe_files"] = "FOILPROBE.loss"
        self.find_da["subs_overrides"] = {
            "__n_turns__":50.1,
            "__no_field_maps__":"// ",
            "__max_y_power__":6
        }
        self.find_da["required_n_hits"] = 50
        self.substitution_list = get_substitution_list()
        print "Running", len(self.substitution_list), "substitutions"

