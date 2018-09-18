import os
import json
import math

import config_base

def get_end(theta):
    return 1.0*(1.5/math.cos(math.radians(41))/2.)/theta

def get_substitution_list():
    substitution_list = []
    for end_length in range(2, 13):
        f_end_length = get_end(2.4)
        d_end_length = get_end(4.8)
        sub = config_base.get_baseline_substitution()
        sub["__d_end_length__"] = d_end_length*end_length/5.
        sub["__f_end_length__"] = f_end_length*end_length/5.
        substitution_list.append(sub)
    print json.dumps(substitution_list, indent=2)
    return substitution_list

class Config(config_base.Config):
    pass
    
Config.substitution_list = get_substitution_list()
Config.run_control["output_dir"] = os.path.join(os.getcwd(), "output/end_length")
