import os
import config_base

class Config(config_base.Config):
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
    
Config.run_control["find_tune"] = True
Config.run_control["find_da"] = False
Config.run_control["output_dir"] = os.path.join(os.getcwd(), "output/baseline_tune")
