import math
import os
import config_base

def get_baseline_substitution():
    baseline = {
        "__energy__":11., # MeV
        "__beamfile__":'disttest.dat',
        "__step_size__":10., # mm
        "__n_turns__":2.1,
        "__n_events__":1,
        "__no_field_maps__":"// ", # set to "" to enable field maps; set to "// " to comment them
        "__probe_angle__":math.pi/6.,
    }
    return baseline

class Config(object):
    def __init__(self):
        self.find_closed_orbits = {
            "seed":[[4.60193762e+03, 0.],],
            "output_file":"find_closed_orbit",
            "subs_overrides":{"__n_turns__":2.1, "__no_field_maps__":""},
            "root_batch":0,
            "max_iterations":5,
            "do_plot_orbit":True,
            "run_dir":"tmp/find_closed_orbits/",
            "probe_files":"PROBE*.loss",
        }
        self.find_tune = {
            "run_dir":"tmp/find_tune/",
            "probe_files":"PROBE0.loss",
            "subs_overrides":{"__n_turns__":50.1},
            "root_batch":0,
            "delta_x":2.,
            "delta_y":1.,
            "max_n_cells":0.1,
            "output_file":"find_tune",
            "row_list":None,
            "axis":None,
        }
        self.find_da = {
            "run_dir":"tmp/find_da/",
            "probe_files":"PROBE1.loss",
            "subs_overrides":{"__n_turns__":500.1},
            "get_output_file":"get_da",
            "scan_output_file":"scan_da",
            "row_list":None,
            "scan_x_list":[],
            "scan_y_list":[],
            "x_seed":None,
            "y_seed":1.,
            "min_delta":1.0,
            "max_delta":500.,
            "required_n_hits":500,
            "max_iterations":10.,
        }
        self.find_rf_parameters = {
            "run_dir":"tmp/find_rf/",
            "probe_files":"PROBE1.loss", # for phase determination
            "do_co_scan":False,
            "delta_energy_list":[2.5, 2.9, 3.1, 3.5],
            # potential BUG here; - not sure if __rf_voltage__ 0 screws things up
            "phasing_subs_overrides":{"__n_turns__":2.1, "__no_field_maps__":"// ", "__rf_voltage__":0.},
            "final_subs_overrides":{"__n_turns__":400.1, "__no_field_maps__":""},
            "start_energy":3.0,
            "end_energy":30,
            "n_steps":10,
            "n_cells":15,
            "v_peak":100, #kV
            "freq_polynomial":2, #linear fit
            "phi_s":math.radians(20),
        }
        
        # Ack! its now hanging when I use mpirun. sigh, I must have broken something.
        # 2000 event-turns took ~ 30 minutes on one core (=> 24 hours per 100,000 event-turns per core) with no space charge
        # 100,000 event-turns took ~ 6 hours on 4 cores (=> 24 hours per 100,000 event-turns per core) with no space charge
        self.track_beam = {
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

        self.substitution_list = [get_baseline_substitution()]
        
        self.run_control = {
            "find_closed_orbits":False,
            "find_tune":True,
            "find_da":False,
            "find_rf_parameters":False,
            "track_beam":False,
            "clean_output_dir":False,
            "output_dir":os.path.join(os.getcwd(), "output/kurri"),
        }

        self.tracking = {
            "mpi_exe":None, #os.path.expandvars("${OPAL_ROOT_DIR}/external/install/bin/mpirun"),
            "n_cores":4,
            "lattice_file":os.path.join(os.getcwd(), "lattice/kurri_main_ring/Kurri_ADS_Ring.in"),
            "opal_path":os.path.expandvars("${OPAL_EXE_PATH}/opal"),
            "step_size":1.,
            "pdg_pid":2212,
        }

