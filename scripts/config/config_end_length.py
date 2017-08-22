import os
import json

import config_base

def get_substitution_list():
    substitution_list = []
    for end_length in [0.01, 0.02, 0.04, 0.06, 0.08, 0.1]:
        sub = config_base.get_baseline_substitution()
        sub["__end_length__"] = end_length
        substitution_list.append(sub)
    print json.dumps(substitution_list, indent=2)
    return substitution_list

class Config(config_base.Config):
    pass
    
Config.substitution_list = get_substitution_list()
Config.run_control["output_dir"] = os.path.join(os.getcwd(), "output/end_length")
