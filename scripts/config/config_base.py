import math
import os

"""
This configuration will attempt to find the closed orbit, tune and dynamic
aperture for a single configuration. It is the basic configuration that is used
for the scripting part of this tutorial.
"""

def get_baseline_substitution(r_inj=4000.0, delta=41.0, r_0=4000.0):
    dphi = math.tan(math.radians(delta))*math.log(r_inj/r_0)
    baseline = {
        # beam
        "__energy__":2.55, # reference trajectory kinetic energy [MeV]
        "__beam_theta__":0., # initial beam alignment [degree]
        "__beam_charge__":1., # beam charge [proton charge]
        "__beam_phi_init__":0.0, # initial beam azimuthal position [degree]
        "__beamfile__":'disttest.dat', # file used for beam position
        "__current__":1.6e-19, # initial beam current [C]
        "__n_events__":1, # number of events
        "__lattice_phi_offset__":math.degrees(dphi), # initial lattice azimuthal position[degree]
        # tracking
        "__step_size__":1., # mm; this is the step size at 2.55 MeV
        "__n_turns__":2.1, # number of turns to track
        # main magnets
        "__b_mean__":0.492, # mean dipole field [T]
        "__df_ratio__":-0.36, # ratio between d and f fields
        "__d_length__":0.1, # length of d magnet [proportion of cell length]
        "__f_length__":0.2, # length of f magnet [proportion of cell length]
        "__d_end_length__":(1.0/math.cos(math.radians(delta)))/1.0/2.4,  # length of d fringe field
        "__f_end_length__":(1.0/math.cos(math.radians(delta)))/3.65/4.8,  # length of f fringe field
        "__tan_delta__":-math.tan(math.radians(abs(delta))), # spiral angle tangent
        "__field_index__":7.1, # field index k
        "__max_y_power__":2, # maximum vertical power of the field expansion
        "__neg_extent__":1.0, # negative radial extent
        "__pos_extent__":1.0, # positive radial extent
    }
    return baseline

class Config(object):
    def __init__(self):
        self.find_closed_orbits = {
            "seed":[[4100., -7.29035424]], # 2.55 MeV
            "output_file":"find_closed_orbit.json",
            "subs_overrides":{"__n_turns__":1.1, "__no_field_maps__":""},
            "root_batch":0,
            "max_iterations":5,
            "run_dir":"tmp/find_closed_orbits/",
            "probe_files":"RINGPROBE*.loss",
        }
        self.find_tune = {
            "run_dir":"tmp/find_tune/",
            "probe_files":"RINGPROBE*.loss",
            "subs_overrides":{"__n_turns__":1.1,
                              "__no_field_maps__":"// ",
                              "__step_size__":0.1},
            "root_batch":0,
            "delta_x":1.,
            "delta_y":1.,
            "max_n_cells":0.1,
            "output_file":"find_tune.json",
            "row_list":None,
            "axis":None,
        }
        self.find_da = {
            "run_dir":"tmp/find_da/",
            "probe_files":"RINGPROBE*.loss",
            "subs_overrides":{"__n_turns__":6.1, "__no_field_maps__":"// "},
            "get_output_file":"get_da.json",
            "scan_output_file":"scan_da.json",
            "row_list":None,
            "scan_x_list":[],
            "scan_y_list":[],
            "x_seed":100.0,
            "y_seed":20.0,
            "min_delta":0.01,
            "max_delta":500.,
            "required_n_hits":50,
            "max_iterations":10,
        }

        self.substitution_list = [get_baseline_substitution()]
        
        self.run_control = {
            "find_closed_orbits":True,
            "find_tune":True,
            "find_da":True,
            "output_dir":os.path.join(os.getcwd(), "output/base"),
            "clean_output_dir":False,
        }

        self.tracking = {
            "mpi_exe":None, #os.path.expandvars("${OPAL_ROOT_DIR}/external/install/bin/mpirun"),
            "beam_file_out":"disttest.dat",
            "n_cores":4,
            "lattice_file":os.path.join(os.getcwd(), "lattice/FETS_Ring.in"),
            "lattice_file_out":"FETS_Ring.opal",
            "opal_path":os.path.expandvars("${OPAL_EXE_PATH}/opal"),
            "tracking_log":"log",
            "step_size":1.,
            "pdg_pid":2212,
            "clear_files":"*.loss",
        }

