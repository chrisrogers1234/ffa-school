import os
import json

from . import config_reference

def get_substitution_list():
    substitution_list = []
    for index in range(5):
        sub = config_reference.get_baseline_substitution()
        sub["__field_index__"] = 20.85+0.01*index
        substitution_list.append(sub)
    print(json.dumps(substitution_list, indent=2))
    return substitution_list

class Config(config_reference.Config):
    pass
    
Config.substitution_list = get_substitution_list()
Config.run_control["output_dir"] = os.path.join(os.getcwd(), "reference/field_index")
