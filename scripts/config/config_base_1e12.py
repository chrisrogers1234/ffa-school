import os
from . import config_base

class Config(config_base.Config):
    pass

Config.tracking["mpi_exe"] = None #os.path.expandvars("${OPAL_ROOT_DIR}/external/install/bin/mpirun")
Config.track_beam["subs_overrides"]["__current__"] = 1.6e-19*1e12
Config.run_control["output_dir"] = os.path.join(os.getcwd(), "output/baseline_1e12")
