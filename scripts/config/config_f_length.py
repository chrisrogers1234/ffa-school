import os
import json

from . import config_base

def get_substitution_list():
    substitution_list = []
    for index in range(6):
        sub = config_base.get_baseline_substitution()
        sub["__f_length__"] = 0.05+0.05*index
        substitution_list.append(sub)
    print(json.dumps(substitution_list, indent=2))
    return substitution_list

class Config(config_base.Config):
    pass
    
Config.substitution_list = get_substitution_list()
Config.run_control["output_dir"] = os.path.join(os.getcwd(), "output/f_length")
