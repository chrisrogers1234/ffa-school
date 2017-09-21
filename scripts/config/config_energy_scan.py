import os
import json

import config_base

def get_substitution_list():
    substitution_list = []
    for index in [3, 4, 5, 6, 7]+range(8, 13, 2)+range(15, 31, 3):
        sub = config_base.get_baseline_substitution()
        sub["__energy__"] = float(index)
        substitution_list.append(sub)
    print json.dumps(substitution_list, indent=2)
    return substitution_list

class Config(config_base.Config):
    pass
    
Config.substitution_list = get_substitution_list()
Config.run_control["output_dir"] = os.path.join(os.getcwd(), "output/energy_tandelta=1")
