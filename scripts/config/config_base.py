import os
import config_base

def get_baseline_substitution():
    baseline = {
        "__end_length__":0.05,
        "__tan_delta__":0.5,
        "__field_index__":15,
        "__max_y_power__":10,
        "__energy__":3.,
        "__beamfile__":'disttest.dat',
        "__step_size__":10.,
        "__n_turns__":2.,
    }
    return baseline

class Config(object):
    find_closed_orbits = {
        "seed":[3000., 0.0, 0.],
        "output_file":"find_closed_orbit",
        "subs_overrides":{"__n_turns__":2.1},
        "root_batch":0,
        "pdg_pid":2212,
        "run_dir":"tmp/find_closed_orbits/",
        "probe_files":"PROBE*.loss",
    }
    
    find_tune = {
        "run_dir":"tmp/find_tune/",
        "probe_files":"PROBE*.loss",
        "subs_overrides":{"__n_turns__":10.1},
        "root_batch":0,
        "delta_x":10.,
        "delta_y":10.,
        "output_file":"find_tune",
        "row_list":None,
        "axis":None,
    }
    
    find_da = {
        "run_dir":"tmp/find_da/",
        "probe_files":"PROBE10.loss",
        "subs_overrides":{"__n_turns__":125.1},
        "get_output_file":"get_da",
        "scan_output_file":"scan_da",
        "row_list":None,
        "scan_x_list":[],
        "scan_y_list":[],
        "x_seed":None,
        "y_seed":10.,
        "min_delta":10.,
        "max_delta":500.,
        "required_n_hits":100,
        "max_iterations":10.,
    }

    substitution_list = [get_baseline_substitution()]
    
    run_control = {
        "find_closed_orbits":True,
        "find_tune":True,
        "find_da":True,
        "clean_output_dir":False,
        "output_dir":os.path.join(os.getcwd(), "output/baseline"),
    }

    
    tracking = {
        "lattice_file":os.path.join(os.getcwd(), "lattice/FETS_Ring_8_Sectors.in"),
        "opal_path":os.path.expandvars("${OPAL_EXE_PATH}/opal"),
        "step_size":1.,
    }
    
