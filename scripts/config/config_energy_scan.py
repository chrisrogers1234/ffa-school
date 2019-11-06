import math
import os
from . import config_base as config

class Config(config.Config):
    def __init__(self):
        super(Config, self).__init__()
        self.substitution_list = []
        for energy in [3*i for i in range(1, 11)]:
            self.substitution_list.append(config.get_baseline_substitution())
            self.substitution_list[-1]["__energy__"] = energy
        self.run_control["output_dir"] = os.path.join(os.getcwd(), "output/energy_scan")
        self.run_control["find_tune"] = False
        self.run_control["find_da"] = False

