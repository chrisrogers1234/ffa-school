import os
import json

import config_reference

def get_substitution_list():
    substitution_list = []
    for index in [energy for energy in range(400, 1201, 50)]:
        sub = config_reference.get_baseline_substitution()
        sub["__energy__"] = float(index)
        substitution_list.append(sub)
    print json.dumps(substitution_list, indent=2)
    return substitution_list

class Config(config_reference.Config):
    pass
    
Config.substitution_list = get_substitution_list()
Config.run_control["output_dir"] = os.path.join(os.getcwd(), "reference/energy")
