import xboa.common


class FindFixedFrequency(object):
    def __init__(self, config):
        self.config = config
        self.energy_time_list = []
        self.closed_orbit_list = []
        self.et_fit = []
        self.freq_fit = []
        self.phase_fit = []
        self.reference_et = []
        self.mass = xboa.common.pdg_pid_to_mass[self.config.tracking["pdg_pid"]]
        self.canvases = {}
        self.output_dir = self.config.run_control["output_dir"]
        self.tmp_dir = os.path.join(self.config.run_control["output_dir"],
                               self.config.find_fixed_frequency["run_dir"])
        self.e0 = self.config.find_fixed_frequency["start_energy"]
        print self.tmp_dir
