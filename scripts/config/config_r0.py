import os
import config.config_base as config

def get_substitution_list():
    substitution = config.get_baseline_substitution(4000., 0.0, 4000.)
    print('Phi offset', substitution['__lattice_phi_offset__'])
    return [substitution]

class Config(config.Config):
    def __init__(self):
        super(Config, self).__init__()
        self.substitution_list = get_substitution_list()
        self.find_closed_orbits["max_iterations"] = 5
        self.run_control["find_closed_orbits"] = False
        self.run_control["find_da"] = True
        #self.set_low_energy()
        self.set_high_energy()

    def set_low_energy(self):
        self.run_control["output_dir"] = os.path.join(os.getcwd(), "output/r0")
        self.substitution_list[0]['__energy__'] = 2.55
        self.find_closed_orbits["seed"] = [[3994.15161877, -5.26214738]] # [[4657.8, -18.3]] # 
        self.find_da["x_seed"] = 1. # 4657./3994. #
        self.find_da["y_seed"] = 1. # 4657./3994. #
        self.find_da["subs_overrides"]["__n_turns__"] = 30.1

    def set_high_energy(self):
        self.run_control["output_dir"] = os.path.join(os.getcwd(), "output/r1")
        self.substitution_list[0]['__energy__'] = 30
        self.find_closed_orbits["seed"] = [[4657.8, -18.3]] #
        self.find_da["x_seed"] = 4657./3994. #
        self.find_da["y_seed"] = 4657./3994. #

