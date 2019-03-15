import copy
import os
import json

import config_base as config
DIR = "bump_design_outer-radius_-1_0_1_2_painting"

# 0.21625, 0.21833
def get_substitution_list():
    sub_list = []
    bump_fringe = 0.1
    bump_angle = -41.0
    #for bump_fringe in [0.05, 0.1, 0.2]:
    sub = config.get_baseline_substitution()
    sub["__test_probe__"] = 3.5
    sub["__phi_foil_probe__"] = 3.2
    sub["__phi_bump_1__"] = +0.5
    sub["__phi_bump_2__"] = -0.55
    sub["__phi_bump_3__"] = -1.5
    sub["__phi_bump_4__"] = -2.5
    sub["__bump_field_1__"] = 0.0
    sub["__bump_field_2__"] = 0.0
    sub["__bump_field_3__"] = 0.0
    sub["__bump_field_4__"] = 0.0
    sub["__step_size__"] = 10.0
    sub["__bump_angle__"] = -0.0 # angular tilt of bump cavity
    sub["__bump_fringe__"] = 0.1
    sub["__bump_length__"] = 0.3
    sub["__septum_field__"] = 0.0 # 0.801
    sub_list.append(sub)
    #for bump_angle in [-41]+[-5.*i for i in range(11)]:
    #    my_sub = copy.deepcopy(sub)
    #    my_sub["__bump_angle__"] = bump_angle # angular tilt of bump cavity
    #    sub_list.append(my_sub)
    #for bump_fringe in [0.2-0.025*i for i in range(8)]:
    #    my_sub = copy.deepcopy(sub)
    #    my_sub["__bump_fringe__"] = bump_fringe # angular tilt of bump cavity
    #    sub_list.append(my_sub)
    print "Generated", len(sub_list), "subs:"
    print "    angles: ", [format(my_sub["__bump_angle__"], "6.4f") for my_sub in sub_list]
    print "    fringes:", [format(my_sub["__bump_fringe__"], "6.4f") for my_sub in sub_list]
    return sub_list

class Config(config.Config):
    def __init__(self):
        super(Config, self).__init__()
        self.run_control = {
            "find_closed_orbits":False,
            "find_tune":False,
            "find_da":False,
            "find_rf_parameters":False,
            "find_bump_parameters":True,
            "track_beam":False,
            "track_bump":True,
            "clean_output_dir":False,
            "output_dir":os.path.join(os.getcwd(), "output/"+DIR),
        }
        self.substitution_list = get_substitution_list()
        self.find_closed_orbits["seed"] = [[4042.10640218, -8.47136893],]
        self.find_bump_parameters["closed_orbit"] = [4042.10640218, -8.47136893]
        self.find_bump_parameters["bump"] = [[-20.*i/5+4018.0-4042.1, -8.6771+8.471] for i in range(2)] #-8.471
        self.find_bump_parameters["fix_bumps"] = ["__bump_field_2__"]
        self.find_bump_parameters["seed_field"] = [0.0, -0.04, 0.0, -0.0]
        self.find_bump_parameters["seed_errors"] = [0.001, 0.001, 0.001, 0.001]
        self.find_bump_parameters["foil_probe_phi"] = 3.2
        self.find_bump_parameters["max_iterations"] = 500
        self.find_bump_parameters["position_tolerance"] = 0.1
        self.find_bump_parameters["momentum_tolerance"] = 1000 #0.01
        self.find_bump_parameters["magnet_min_field"] = -1.0
        self.find_bump_parameters["magnet_max_field"] = +1.0
        self.find_bump_parameters["ref_probe_files"] = ["FOILPROBE.loss", "TESTPROBE.loss", "RINGPROBE*.loss"]
        self.find_bump_parameters["ignore_stations"]  = [4, 5, 16]

        # list of bump fields to consider, based on orbit initial trajectory (urk)
        self.track_bump["bump_list"] = [[-20.*i/5+4018.0-4042.1, -8.6771+8.471] for i in reversed(range(2))]
        # this is the bump_list element corresponding to the centroid of the injected
        # beam (i.e. the position of the newly inserted painted beam)
        self.track_bump["injection_orbit"] = -1
        self.track_bump["n_turns_list"] = [1, 5, 25]

        self.tracking["lattice_file"] = os.path.join(os.getcwd(), "lattice/FETS_Ring.test")
