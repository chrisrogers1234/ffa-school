import copy
import os
import json

import config_triplet

# 0.21625, 0.21833
def get_substitution_list():
    substitution_list = []
    sub = config_triplet.get_baseline_substitution()
    for index1 in range(5):
        sub["__field_index__"] = 4-0.5*index1
        substitution_list.append(copy.deepcopy(sub))
    print json.dumps(substitution_list, indent=2)
    return substitution_list

class Config(config_triplet.Config):
    def __init__(self):
        pass

Config.substitution_list = get_substitution_list()
Config.run_control["output_dir"] = os.path.join(os.getcwd(), "output/triplet_scan_3/")
