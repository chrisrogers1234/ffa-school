import os
import json

import config_base

class Config(config_base.Config):
    find_da = {
        "run_dir":"tmp/find_da/",
        "probe_files":"PROBE1.loss",
        "subs_overrides":{"__n_turns__":130.1},
        "get_output_file":"get_da",
        "scan_output_file":"scan_da",
        "row_list":[0],
        "scan_x_list":[5.*i for i in range(0, 11)],
        "scan_y_list":[5.*i for i in range(0, 11)],
        "x_seed":10.,
        "y_seed":10.,
        "min_delta":1.,
        "max_delta":500.,
        "required_n_hits":100,
        "max_iterations":10.,
    }
    
Config.run_control["output_dir"] = os.path.join(os.getcwd(), "output/da_scan")
