import os
import config_base

def get_baseline_substitution():
    baseline = {
        "__end_length__":0.1,
        "__tan_delta__":0.711,
        "__field_index__":4.48,
        "__max_y_power__":4,
        "__energy__":3.,
        "__beamfile__":'disttest.dat',
        "__step_size__":1.,
        "__n_turns__":2.1,
        "__b_mean__":-0.011,
        "__df_ratio__":-0.1965,
        "__d_length__":0.2,
        "__f_length__":0.1,
    }
    return baseline

class Config(object):
    find_closed_orbits = {
        "seed":[2785.65, -7.09738962478, 0.],
        "output_file":"find_closed_orbit",
        "subs_overrides":{"__n_turns__":2.1},
        "root_batch":0,
        "max_iterations":5,
        "pdg_pid":2212,
        "do_plot_orbit":False,
        "run_dir":"tmp/find_closed_orbits/",
        "probe_files":"PROBE*.loss",
    }
    
    find_tune = {
        "run_dir":"tmp/find_tune/",
        "probe_files":"PROBE*.loss",
        "subs_overrides":{"__n_turns__":5.1},
        "root_batch":0,
        "delta_x":2.,
        "delta_y":0.1,
        "max_n_cells":0.1,
        "output_file":"find_tune",
        "row_list":None,
        "axis":None,
    }
    
    find_da = {
        "run_dir":"tmp/find_da/",
        "probe_files":"PROBE1.loss",
        "subs_overrides":{"__n_turns__":500.1},
        "get_output_file":"get_da",
        "scan_output_file":"scan_da",
        "row_list":None,
        "scan_x_list":[],
        "scan_y_list":[],
        "x_seed":10.,
        "y_seed":10.,
        "min_delta":1.0,
        "max_delta":500.,
        "required_n_hits":500,
        "max_iterations":10.,
    }

    substitution_list = [get_baseline_substitution()]
    
    run_control = {
        "find_closed_orbits":False,
        "find_tune":False,
        "find_da":True,
        "clean_output_dir":False,
        "output_dir":os.path.join(os.getcwd(), "output/baseline"),
    }

    
    tracking = {
        "lattice_file":os.path.join(os.getcwd(), "lattice/FETS_Ring.in"),
        "opal_path":os.path.expandvars("${OPAL_EXE_PATH}/opal"),
        "step_size":1.,
    }
    
