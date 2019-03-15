import os
import json

import config_rf_ff

def get_substitution_list():
    substitution_list = []
    for index in [energy for energy in range(3, 31, 1)]:
        sub = config_rf_ff.get_baseline_substitution()
        sub["__energy__"] = float(index)
        substitution_list.append(sub)
    print json.dumps(substitution_list, indent=2)
    return substitution_list

class Config(config_rf_ff.Config):
    def __init__(self):
        super(Config, self).__init__()
        self.run_control["output_dir"] = os.path.join(os.getcwd(), "output/rf_ff_energy")
        self.substitution_list = get_substitution_list()
