import os
import json

from . import config_reference

# 0.21625, 0.21833
def get_substitution_list():
    substitution_list = []
    for index in range(5):
        sub = config_reference.get_baseline_substitution()
        sub["__b_f__"] = 5.8+0.2*index
        substitution_list.append(sub)
    print(json.dumps(substitution_list, indent=2))
    return substitution_list

class Config(config_reference.Config):
    pass
    
Config.substitution_list = get_substitution_list()
Config.run_control["output_dir"] = os.path.join(os.getcwd(), "reference/b_f")
