import json
import xboa.common

class TrackBeam(object):
    def __init__(self, config):
        self.config = config
        self.output_dir = config.run_control["output_dir"]
        self.x_centre = None
        self.x_ellipse = None
        self.y_centre = None
        self.y_ellipse = None

    def load_tune_data(self):
        file_name = self.output_dir+"/"+self.config.find_tune["output_file"]
        fin = open(file_name)
        data = [json.loads(line) for line in fin.readlines()]
        print len(data)
        print data[0].keys()
        print data[0]['x_signal']
        print data[0]['y_signal']
        return data

    def fit_tune_data(self, data):
        eps_max = self.config.track_beam['eps_max']
        
        self.x_centre, self.x_ellipse = xboa.common.fit_ellipse(
                                                  data['x_signal'],
                                                  eps_max,
                                                  verbose = True)
        self.y_centre, self.y_ellipse = xboa.common.fit_ellipse(
                                                  data['y_signal'],
                                                  eps_max,
                                                  verbose = True)


    def generate_beam(self):
        data = self.load_tune_data()
        for item in data:
            self.fit_tune_data(item)

def main(config):
    tracker = TrackBeam(config)
    tracker.generate_beam()
    