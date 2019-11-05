import os
from . import config_base

class Config(config_base.Config):
    pass

Config.track_beam["subs_overrides"]["__n_events__"] = 10
Config.track_beam["subs_overrides"]["__solver__"] = "NONE"
Config.tracking["mpi_exe"] = os.path.expandvars("${OPAL_ROOT_DIR}/external/install/bin/mpirun")

Config.run_control = {
        "find_closed_orbits":True,
        "find_tune":True,
        "find_da":False,
        "track_beam":True,
        "clean_output_dir":False,
        "output_dir":os.path.join(os.getcwd(), "output/baseline_alt"),
    }

