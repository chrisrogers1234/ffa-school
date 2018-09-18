import math
import os
import config_base

# OPTIMISATION NOTES

# CPU time goes linearly with step size
# CPU time goes linearly with number of turns
# CPU time seems weakly dependent on max y power
# CPU time seems weakly dependent on SPT dump freq

# Implies most of the CPU time is not spent during field lookup. Alternatives:
# * Coordinate transformation
# * RK
# Rebuild using gprof?
# Nb looks like 10 mm step size is okay for tracking


def get_baseline_substitution():
    baseline = {
        "__end_length__":0.1,
        "__tan_delta__":math.tan(math.radians(60)),
        "__field_index__":20.734, #20.969,
        "__max_y_power__":10,
        "__energy__":400.,
        "__beamfile__":'disttest.dat',
        "__step_size__":0.01,
        "__n_turns__":0.011,
        "__b_d__":+10.0,
        "__b_f__":-3.788,
        "__d_length__":0.2, # cell is 15 degrees; magnet is 3 degrees
        "__f_length__":0.1,
        "__n_events__":1,
        "__solver__":"None",
        "__mx__":10,
        "__my__":10,
        "__mt__":5,
        "__current__":1.6e-19,
        "__dump_fields_n_points__":1,
    }
    return baseline
seed = []
for p in range(-50, 51, 10):
    for x in range(7):
        seed.append([23700.+100.*x, p, 0.])

class Config(object):
    find_closed_orbits = {
        "seed":seed, #[[23720., -41.81, 0.]],
        "output_file":"find_closed_orbit",
        "subs_overrides":{"__n_turns__":0.011, "__max_y_power__":1, "__dump_fields_n_points__":360*4/12},
        "root_batch":0,
        "max_iterations":5,
        "do_plot_orbit":False,
        "run_dir":"tmp/find_closed_orbits/",
        "probe_files":"PROBE*.loss",
    }
    
    find_tune = {
        "run_dir":"tmp/find_tune/",
        "probe_files":"PROBE*.loss",
        "subs_overrides":{"__n_turns__":0.501, "__max_y_power__":1, "__step_size__":0.1,},
        "root_batch":0,
        "delta_x":2.,
        "delta_y":1.,
        "max_n_cells":0.1,
        "output_file":"find_tune",
        "row_list":None,
        "axis":None,
    }
    
    find_da = {
        "run_dir":"tmp/find_da/",
        "probe_files":"PROBE1.loss",
        "subs_overrides":{"__n_turns__":1.1, "__step_size__":0.1,},
        "get_output_file":"get_da",
        "scan_output_file":"scan_da",
        "row_list":None,
        "scan_x_list":[],
        "scan_y_list":[],
        "x_seed":10.,
        "y_seed":10.,
        "min_delta":1.0,
        "max_delta":500.,
        "required_n_hits":100,
        "max_iterations":10.,
    }
    
    # Ack! its now hanging when I use mpirun. sigh, I must have broken something.
    # 2000 event-turns took ~ 30 minutes on one core (=> 24 hours per 100,000 event-turns per core) with no space charge
    # 100,000 event-turns took ~ 6 hours on 4 cores (=> 24 hours per 100,000 event-turns per core) with no space charge
    track_beam = {
        "run_dir":"tmp/track_beam/",
        "probe_files":"PROBE1.loss",
        "subs_overrides":{"__n_turns__":10.0, "__n_events__":10, "__step_size__":1.,
                          "__solver__":"None", "__mx__":32, "__my__":32, "__mt__":5, "__current__":1.6e-19*1e0},
        "eps_max":1e9,
        "x_emittance":1e-2,
        "y_emittance":1e-2,
        "sigma_pz":1.e-9,
        "sigma_z":1.e-9,
        "do_track":False,
        "single_turn_plots":range(0, 101, 1),
        "min_radius":100.,
        "max_delta_p":50.,
        "plot_events":[1, 2],
    }

    substitution_list = [get_baseline_substitution()]
    
    run_control = {
        "find_closed_orbits":True,
        "find_tune":False,
        "find_da":False,
        "track_beam":False,
        "clean_output_dir":True,
        "output_dir":os.path.join(os.getcwd(), "reference/reference"),
    }

    tracking = {
        "mpi_exe":None, #os.path.expandvars("${OPAL_ROOT_DIR}/external/install/bin/mpirun"),
        "n_cores":4,
        "lattice_file":os.path.join(os.getcwd(), "lattice/ISIS2_reference.in"),
        "opal_path":os.path.expandvars("${OPAL_EXE_PATH}/opal"),
        "step_size":1.,
        "pdg_pid":2212,
    }
    
