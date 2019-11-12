import math
import os
from . import config_base as config

"""
This configuration runs a parameter scan, using config_base as a basis and
varying the df ratio (ratio of focussing:defoccusing dipole strengths).
"""


class Config(config.Config):
    def __init__(self):
        super(Config, self).__init__()
        # The substitution list controls the scan parameters; the scripts will
        # run once for each element in the substitution list. Here we set the
        # df ratio as a loop parameter.
        self.substitution_list = []
        for i in range(5):
            self.substitution_list.append(config.get_baseline_substitution())
            self.substitution_list[-1]["__df_ratio__"] = -0.3-0.03*i
        self.run_control["output_dir"] = os.path.join(os.getcwd(), "output/scan")
        # make sure the closed orbit and tune calculation are enabled. Disable
        # the DA calculation
        self.run_control["find_closed_orbits"] = True
        self.run_control["find_tune"] = True
        self.run_control["find_da"] = False
        # Set the initial guess at the closed orbit to something close to the
        # true value
        self.find_closed_orbits["seed"] = [[4000., -7.29035424]]


